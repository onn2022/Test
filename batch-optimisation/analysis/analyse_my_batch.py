#!/usr/bin/env python3
"""
Profile the Cardlink MY (MY20A2 / TMYCLKA7) batch and rank tuning targets.

Reads the CSVs produced by extract_repository.py and writes the evidence pack
under ../reports.  Every recommendation in docs/MY_BATCH_OPTIMISATION.md is
derived from one of these reports - nothing is asserted without a row behind it.

Reports produced:
    00_summary.md                   headline numbers for the CAB pack
    01_top_consumers.csv            biggest per-cycle elapsed-time consumers
    02_instability.csv              jobs whose worst run dwarfs their average
    03_critical_path.csv            longest parsed OPC chain, per plan
    04_plan_profile.csv             work and chain length per A7 plan
    05_sort_dynalloc_candidates.csv SORT/ICETOOL members with no DYNALL* member
    06_sort_intermediates.csv       members landing sort output on permanent DASD
    07_copy_candidates.csv          IEBGENER members still to move to ICEGENER
    09_priority_targets.csv         tuning signals joined to measured runtime

Usage:
    python3 analyse_my_batch.py [--datadir data] [--outdir ../reports]
"""

import argparse
import csv
import os
import re
from collections import Counter, defaultdict, deque

CYCLES_JUN26 = 32          # daily cycles observed in the Jun-2026 statistics
SORT_PROGRAMS = ('SORT', 'ICETOOL', 'ICEMAN', 'SYNCSORT')
INTERMEDIATE_RE = re.compile(r'\.(SORT\d*|SRT\d*|SORTED)$')


def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def load(datadir, name):
    with open(os.path.join(datadir, name), encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def write_csv(outdir, name, header, rows):
    path = os.path.join(outdir, name)
    with open(path, 'w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)
    return path


# ------------------------------------------------------------------ analyses

def plan_profile(jobs):
    """Work per A7 plan: job count, summed average and P95 elapsed minutes."""
    totals = defaultdict(lambda: [0, 0.0, 0.0])
    for job in jobs:
        bucket = totals[job['Application/Plan']]
        bucket[0] += 1
        bucket[1] += number(job['Avg Runtime Jun-26 (min)'])
        bucket[2] += number(job['P95 Runtime Jun-26 (min)'])
    return totals


def critical_paths(jobs, deps):
    """
    Longest parsed OPC chain per plan (CPM on the explicit dependency edges).

    Only the 536 MY relationships the repository marks 'Parsed' are edges here;
    continuation-only OPC lines were never recovered, so a chain is a proven
    lower bound on that plan's elapsed time, never an upper bound.
    """
    duration, plan = {}, {}
    for job in jobs:
        name = job['A7 Job Name'].strip()
        if not name:
            continue
        duration[name] = (number(job['Avg Runtime Jun-26 (min)'])
                          or number(job['Expected Duration (min)']))
        plan[name] = job['Application/Plan']

    edges = [(dep['Predecessor A7 Job'].strip(),
              dep['Successor A7 Job'].strip(),
              number(dep['Lag (min)'])) for dep in deps]
    edges = [edge for edge in edges if edge[0] and edge[1]]

    results = {}
    for target in sorted(set(plan.values())):
        members = {name for name in plan if plan[name] == target}
        successors, indegree = defaultdict(list), Counter({name: 0 for name in members})
        for head, tail, lag in edges:
            if head in members and tail in members:
                successors[head].append((tail, lag))
                indegree[tail] += 1

        pending = dict(indegree)
        queue = deque(name for name in members if pending[name] == 0)
        order = []
        while queue:
            name = queue.popleft()
            order.append(name)
            for tail, _lag in successors[name]:
                pending[tail] -= 1
                if pending[tail] == 0:
                    queue.append(tail)

        start = {name: 0.0 for name in members}
        came_from = {}
        for name in order:
            for tail, lag in successors[name]:
                candidate = start[name] + duration.get(name, 0.0) + lag
                if candidate > start[tail]:
                    start[tail] = candidate
                    came_from[tail] = name
        finish = {name: start[name] + duration.get(name, 0.0) for name in members}
        if not finish:
            continue

        last = max(finish, key=lambda name: finish[name])
        chain, cursor = [], last
        while cursor:
            chain.append(cursor)
            cursor = came_from.get(cursor)
        chain.reverse()
        results[target] = {
            'jobs': len(members),
            'work': sum(duration.get(name, 0.0) for name in members),
            'chain_minutes': finish[last],
            'chain': [(name, duration.get(name, 0.0), start[name], finish[name])
                      for name in chain],
        }
    return results


def jcl_signals(inventory):
    """Split the captured JCL evidence into the three JCL-level tuning buckets."""
    dynalloc, intermediates, iebgener = [], [], []
    for member in inventory:
        programs = member['Executed Programs'].split()
        datasets = member['Datasets (max 50)'].split()
        name = member['JCL Member']

        sorts = [p for p in programs if p in SORT_PROGRAMS]
        has_dynall = any('DYNALL' in dataset for dataset in datasets)
        if sorts and not has_dynall:
            dynalloc.append((name, ' '.join(sorts), len(datasets),
                             member['First Evidence Line'], member['Last Evidence Line']))

        landed = [dataset for dataset in datasets if INTERMEDIATE_RE.search(dataset)]
        if landed:
            intermediates.append((name, len(landed), len(datasets), ' '.join(landed[:6])))

        if 'IEBGENER' in programs:
            iebgener.append((name, ' '.join(programs), len(datasets)))
    return dynalloc, intermediates, iebgener


# ---------------------------------------------------------------------- main

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--datadir', default=os.path.join(here, 'data'))
    parser.add_argument('--outdir', default=os.path.join(here, os.pardir, 'reports'))
    args = parser.parse_args()
    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)

    all_jobs = load(args.datadir, 'Batch_Jobs.csv')
    deps = [d for d in load(args.datadir, 'Batch_Dependencies.csv') if d['Region'] == 'MY']
    runtime = load(args.datadir, 'Runtime_Stats_Jun26.csv')
    inventory = load(args.datadir, 'JCL_Inventory_MY.csv')

    jobs = [j for j in all_jobs if j['Region'] == 'MY']
    live = [j for j in jobs if j['Implementation Status'] == 'Implemented']

    for row in runtime:
        row['avg'] = number(row['Average min'])
        row['p95'] = number(row['P95 min'])
        row['low'] = number(row['Minimum min'])
        row['high'] = number(row['Maximum min'])
        row['runs'] = int(number(row['Runs']))

    # ---- 01 top consumers ------------------------------------------------
    ranked = sorted(runtime, key=lambda r: -r['avg'] * r['runs'])
    write_csv(outdir, '01_top_consumers.csv',
              ['production_job', 'runs', 'avg_min', 'p95_min', 'min_min', 'max_min',
               'total_min_jun26', 'mapped_to_a7'],
              [[r['Production Job'], r['runs'], '%.2f' % r['avg'], '%.2f' % r['p95'],
                '%.2f' % r['low'], '%.2f' % r['high'], '%.0f' % (r['avg'] * r['runs']),
                r['Mapped to A7']] for r in ranked[:120]])

    # ---- 02 instability --------------------------------------------------
    steady = [r for r in runtime if r['runs'] >= 20 and r['avg'] >= 1.0]
    unstable = sorted(steady, key=lambda r: -(r['high'] / r['avg']))
    write_csv(outdir, '02_instability.csv',
              ['production_job', 'runs', 'avg_min', 'p95_min', 'min_min', 'max_min',
               'max_over_avg', 'worst_night_excess_min', 'mapped_to_a7'],
              [[r['Production Job'], r['runs'], '%.2f' % r['avg'], '%.2f' % r['p95'],
                '%.2f' % r['low'], '%.2f' % r['high'], '%.2f' % (r['high'] / r['avg']),
                '%.1f' % (r['high'] - r['avg']), r['Mapped to A7']]
               for r in unstable[:80]])

    # ---- 03/04 plans and chains -----------------------------------------
    profile = plan_profile(live)
    paths = critical_paths(jobs, deps)
    write_csv(outdir, '04_plan_profile.csv',
              ['plan', 'live_jobs', 'work_min_avg', 'work_min_p95',
               'longest_parsed_chain_min', 'chain_jobs'],
              [[plan, data[0], '%.1f' % data[1], '%.1f' % data[2],
                '%.1f' % paths.get(plan, {}).get('chain_minutes', 0.0),
                len(paths.get(plan, {}).get('chain', []))]
               for plan, data in sorted(profile.items(), key=lambda kv: -kv[1][1])])

    chain_rows = []
    for plan in sorted(paths):
        for position, (name, dur, begins, ends) in enumerate(paths[plan]['chain'], 1):
            chain_rows.append([plan, position, name, '%.2f' % dur,
                               '%.1f' % begins, '%.1f' % ends])
    write_csv(outdir, '03_critical_path.csv',
              ['plan', 'position', 'a7_job', 'duration_min',
               'earliest_start_min', 'earliest_finish_min'], chain_rows)

    # ---- 05/06/07 JCL-level signals -------------------------------------
    dynalloc, intermediates, iebgener = jcl_signals(inventory)
    write_csv(outdir, '05_sort_dynalloc_candidates.csv',
              ['jcl_member', 'sort_programs', 'dataset_count',
               'first_evidence_line', 'last_evidence_line'],
              sorted(dynalloc))
    write_csv(outdir, '06_sort_intermediates.csv',
              ['jcl_member', 'permanent_sort_datasets', 'dataset_count', 'examples'],
              sorted(intermediates, key=lambda row: -row[1]))
    write_csv(outdir, '07_copy_candidates.csv',
              ['jcl_member', 'executed_programs', 'dataset_count'], sorted(iebgener))

    # ---- 09 priority targets --------------------------------------------
    # A tuning signal only matters where there is elapsed time to recover, so
    # join the JCL signals back onto the Jun-26 statistics and rank by average.
    measured = {row['Production Job']: row for row in runtime}
    needs_dynalloc = {row[0] for row in dynalloc}
    lands_sort = {row[0]: row[1] for row in intermediates}
    targets = []
    for member in sorted(needs_dynalloc | set(lands_sort)):
        stats = measured.get(member)
        if not stats or stats['avg'] <= 0:
            continue
        targets.append([member, stats['runs'], '%.2f' % stats['avg'], '%.2f' % stats['p95'],
                        '%.2f' % stats['high'], 'Y' if member in needs_dynalloc else '',
                        lands_sort.get(member, 0), stats['Mapped to A7'],
                        '%.0f' % (stats['avg'] * stats['runs'])])
    targets.sort(key=lambda row: -float(row[2]))
    write_csv(outdir, '09_priority_targets.csv',
              ['jcl_member', 'runs', 'avg_min', 'p95_min', 'max_min', 'needs_dynalloc',
               'permanent_sort_datasets', 'mapped_to_a7', 'total_min_jun26'], targets)
    target_minutes = sum(float(row[2]) for row in targets)

    # ---- 00 summary ------------------------------------------------------
    work_avg = sum(number(j['Avg Runtime Jun-26 (min)']) for j in live)
    work_p95 = sum(number(j['P95 Runtime Jun-26 (min)']) for j in live)
    work_dec = sum(number(j['Avg Runtime Dec-25 (min)']) for j in live)
    estate = sum(r['avg'] * r['runs'] for r in runtime) / CYCLES_JUN26
    headroom = sum(r['p95'] - r['avg'] for r in steady if r['p95'] > r['avg'])
    sort_members = [m for m in inventory
                    if any(p in SORT_PROGRAMS for p in m['Executed Programs'].split())]

    lines = [
        '# MY batch profile - Jun-2026 statistics',
        '',
        'Generated by `analysis/analyse_my_batch.py` from the Cardlink Batch Dependency',
        'Repository (DOC0148 v5 reviewed). Region MY, production region MY20A2.',
        '',
        '## Estate',
        '',
        '| Metric | Value |',
        '| --- | --- |',
        '| MY jobs in the A7 plans | %d |' % len(jobs),
        '| ... implemented in production | %d |' % len(live),
        '| ... flagged Critical | %d |' % sum(1 for j in jobs if j['Criticality'] == 'Critical'),
        '| ... development only | %d |' % sum(1 for j in jobs if j['Criticality'] == 'Development only'),
        '| Parsed OPC dependencies (MY) | %d |' % len(deps),
        '| Production jobs with Jun-26 statistics | %d |' % len(runtime),
        '| ... mapped onto an A7 operation | %d |' % sum(1 for r in runtime if r['Mapped to A7'] == 'Yes'),
        '',
        '## Elapsed time per cycle',
        '',
        '| Metric | Minutes | Hours |',
        '| --- | ---: | ---: |',
        '| MY plan work, sum of averages | %.1f | %.2f |' % (work_avg, work_avg / 60),
        '| MY plan work, sum of P95 | %.1f | %.2f |' % (work_p95, work_p95 / 60),
        '| MY plan work, Dec-25 averages | %.1f | %.2f |' % (work_dec, work_dec / 60),
        '| Whole MY estate per cycle (all production jobs) | %.1f | %.2f |' % (estate, estate / 60),
        '',
        'Jun-26 is **%+.1f min (%+.1f%%)** against Dec-25 on the same job set.'
        % (work_avg - work_dec, 100.0 * (work_avg - work_dec) / work_dec if work_dec else 0.0),
        '',
        '## Where the time sits',
        '',
        '| Plan | Live jobs | Work (min) | Longest parsed chain (min) |',
        '| --- | ---: | ---: | ---: |',
    ]
    for plan, data in sorted(profile.items(), key=lambda kv: -kv[1][1]):
        lines.append('| %s | %d | %.1f | %.1f |'
                     % (plan, data[0], data[1], paths.get(plan, {}).get('chain_minutes', 0.0)))
    lines += [
        '',
        '## Tuning surface in the captured JCL evidence',
        '',
        '| Signal | Members |',
        '| --- | ---: |',
        '| JCL members captured (of 2,475 in the sheet) | %d |' % len(inventory),
        '| ... running SORT / ICETOOL | %d |' % len(sort_members),
        '| ... running SORT with no DYNALL* control member | %d |' % len(dynalloc),
        '| ... landing sort output on permanent DASD | %d |' % len(intermediates),
        '| ... still running IEBGENER | %d |' % len(iebgener),
        '',
        'Joined to the Jun-26 statistics, **%d members** carrying **%.0f min** of measured'
        % (len(targets), target_minutes),
        'elapsed time per cycle have at least one of those signals (09_priority_targets.csv).',
        '',
        'Stability: the %d jobs with >=20 runs and >=1 min average carry **%.0f min**'
        % (len(steady), headroom),
        'of P95-over-average headroom per cycle - the swing an operator must budget for.',
        '',
    ]
    with open(os.path.join(outdir, '00_summary.md'), 'w', encoding='utf-8') as handle:
        handle.write('\n'.join(lines))

    print('reports written to %s' % outdir)
    for name in sorted(os.listdir(outdir)):
        print('  %s' % name)


if __name__ == '__main__':
    main()

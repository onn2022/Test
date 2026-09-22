#!/usr/bin/env python3
"""
Extract the Cardlink Batch Dependency Repository into normalised CSVs.

Input  : the Google Drive export of
         "DOC0148 Cardlink_Batch_Dependency_Repository_Complete_MY_SG_v5_reviewed"
         (markdown rendering, pipe tables, one "## Sheet: <name>" heading per sheet)
         or the flattened text rendering of the equivalent .xlsx.

Output : analysis/data/<sheet>.csv, one file per sheet, header row preserved.

The repository is the only machine-readable record of the MY/SG A7 and H9 scheduler
plans together with Dec-2025 and Jun-2026 execution statistics, so every number in
the optimisation report is traceable back to it.

Usage:
    python3 extract_repository.py --input DOC0148.md [--outdir data]
"""

import argparse
import csv
import os
import re
import sys

SHEET_RE = re.compile(r'^\\?#\\?#\s*Sheet:\s*(.+?)\s*$')
RULE_RE = re.compile(r'^\|\s*:?-{2,}')


def unescape(text):
    """The Drive renderer backslash-escapes _ # & * in every cell."""
    return re.sub(r'\\(.)', r'\1', text)


def split_sheets(lines):
    """Return {sheet_name: [raw lines]} for every '## Sheet: x' heading."""
    sheets, current = {}, None
    for line in lines:
        probe = line.replace('\\#', '#').strip()
        match = SHEET_RE.match(probe)
        if match:
            current = unescape(match.group(1)).strip()
            sheets[current] = []
            continue
        if current is not None:
            sheets[current].append(line.rstrip())
    return sheets


def rows_from_markdown(body):
    """
    Rejoin wrapped table rows, then split on '|'.

    A logical row starts with '|'. Cells holding multi-line values (dataset lists,
    program lists) wrap onto continuation lines that do NOT start with '|', so they
    are folded back into the row they belong to.
    """
    buffer, raw_rows = [], []
    for line in body:
        text = line.strip()
        if not text:
            continue
        if text.startswith('|'):
            if buffer:
                raw_rows.append(' '.join(buffer))
            buffer = [text]
        elif buffer:
            buffer.append(text)
    if buffer:
        raw_rows.append(' '.join(buffer))

    records = []
    for raw in raw_rows:
        if RULE_RE.match(raw):
            continue
        cells = [unescape(cell).strip() for cell in raw.strip().strip('|').split('|')]
        records.append(cells)
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--input', required=True, help='Drive export of the repository')
    parser.add_argument('--outdir', default=os.path.join(os.path.dirname(__file__), 'data'))
    args = parser.parse_args()

    with open(args.input, encoding='utf-8') as handle:
        lines = handle.read().split('\n')

    sheets = split_sheets(lines)
    if not sheets:
        sys.exit('No "## Sheet:" headings found - is this the markdown rendering?')

    os.makedirs(args.outdir, exist_ok=True)
    for name, body in sheets.items():
        records = rows_from_markdown(body)
        if not records:
            continue
        width = max(len(record) for record in records)
        records = [record + [''] * (width - len(record)) for record in records]
        path = os.path.join(args.outdir, name.replace('/', '_') + '.csv')
        with open(path, 'w', newline='', encoding='utf-8') as handle:
            csv.writer(handle).writerows(records)
        print('%-24s rows=%-6d cols=%-3d -> %s' % (name, len(records) - 1, width, path))


if __name__ == '__main__':
    main()

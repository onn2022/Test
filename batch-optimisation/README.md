# Cardlink MY batch optimisation

Evidence-driven tuning of the Cardlink II MY (`MY20A2` / `TMYCLKA7`) nightly batch,
built from the Cardlink source snapshot and the batch dependency repository held in
Google Drive.

**Start here:** [`docs/MY_BATCH_OPTIMISATION.md`](docs/MY_BATCH_OPTIMISATION.md)

## Layout

```
analysis/
  extract_repository.py   Drive export -> normalised CSVs
  analyse_my_batch.py     CSVs -> the report pack
  data/                   extracted sheets (Batch_Jobs, Batch_Dependencies,
                          Runtime_Stats_Jun26, JCL_Inventory_MY)
reports/                  generated evidence, regenerate any time
jcl/
  DYNALL64.ctl            DFSORT control member for the large master sorts
  PATTERNS.jcl            seven tuned step patterns, copy-ready
  JMYBTUNE.jcl            UAT A/B harness proving output equivalence
docs/
  MY_BATCH_OPTIMISATION.md   findings, recommendations, IA triage
  CHANGESET_01.md            seven line-level changes, exact before/after
```

`reports/00_summary.md` and `10_longpole_findings.md` are the two worth reading first:
the estate profile, and what the four biggest jobs actually do step by step.

## Regenerating the analysis

```sh
python3 analysis/extract_repository.py --input <DOC0148 export>.md
python3 analysis/analyse_my_batch.py
```

No third-party packages — Python 3.8+ standard library only.

`analysis/data/` is committed output. It came from the Drive renderings of DOC0148, both of
which truncate at roughly 1 MB — so `JCL_Inventory_MY.csv` holds 731 of the sheet's 2,475
members, merged from the markdown rendering (137 members) and the `.xlsx` text rendering
(730), which cut off at different points. The other sheets are complete.

Running the extractor against the full `.xlsx` on a workstation recovers the remaining JCL
members and the SG sheets; everything downstream reruns unchanged. See §7 of the main
document for what that gap does and does not affect.

## Validating the JCL

The JCL artifacts are checked against the Impact Analysis Checklist v3 automated rules:

```sh
python3 <cardlink-change-safety>/scripts/ia_check.py --after jcl/PATTERNS.jcl --lang jcl
```

Current results are in [`reports/08_ia_checker.md`](reports/08_ia_checker.md):
`PATTERNS.jcl` **GO**, `JMYBTUNE.jcl` **GO WITH CONDITIONS** (one annotated WARN).

## Status

Analysis and artifacts only. **Nothing here has been executed on a mainframe**, and no
production member has been changed. The intended route is UAT (`MY20A6`) via the JCL
Converter, proved with `JMYBTUNE`, before any RFC is raised.

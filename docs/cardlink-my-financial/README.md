# Cardlink MY — Financial Computations

Compiles the money calculations performed by the Cardlink II Malaysia COBOL system into a
single, simplified Excel reference: `Cardlink_MY_Financial_Computations.xlsx`.

## Source

- Repository: `Cardlink-Source / Current / MY`, snapshot `retrofit-mychg-20260919`
- Read from Google Drive, folder `extracted_MY_members`
- Snapshot date: 19 September 2026

## What the workbook contains

| Sheet | Contents |
| --- | --- |
| Read Me | Purpose, source, method, scope and limitations |
| Financial Formulas | 98 computations: plain-English rule, COBOL as written, program / paragraph / line |
| Summary | Counts by domain, for the catalogue and for the raw scan |
| Parameters & Rates | 43 control-table and master-file fields that drive the formulas |
| Programs | The 20 programs read in full (232,419 lines), with role and statement counts |
| Arithmetic Detail | Every arithmetic statement extracted from those 20 programs |
| MY Scan Coverage | All 4,667 MY members containing arithmetic, for coverage assessment |

## Method

1. A repository-wide scan ranked members by arithmetic statements carrying monetary keywords
   (86,996 statements across 4,667 members; 29,239 with a monetary keyword in 1,359 members).
2. The top-ranked programs were parsed in fixed COBOL format — columns 8-72, column-7 comment
   lines ignored, continuation lines joined up to 18 physical lines per statement.
3. Statements were classified by target field, enclosing paragraph and operands.
4. The distinct formulas per domain were read in context, including the selecting `IF`
   conditions, written up in plain English, and re-verified against the cited source line.

## Limitations

- The 20 programs read in full hold roughly half the monetary arithmetic in the MY repository.
  Remaining members are inventoried but were not read line by line.
- Copybooks were not expanded; arithmetic in a copybook is attributed to the copybook.
- Branches were read, not executed. Which formula fires for a given account depends on product
  configuration and runtime flags.
- Rate and limit *values* live in control tables, not in code. The workbook names the fields;
  current values must come from the production tables.
- Commented-out source was excluded. Several interest paragraphs carry commented history
  (`XXX`, `***`) showing superseded logic; only the live path is documented.

## Reproducing

```
tools/scan_source.py    # repository-wide arithmetic inventory (run against the MY snapshot)
tools/extract.py        # parse the downloaded members, classify each statement
tools/catalogue.py      # the 98 simplified computations, with source anchors
tools/build_xlsx.py     # assemble the workbook
```

`extract.py` and `build_xlsx.py` expect the member `.txt` files in a sibling `data/` directory.

## Verification

- Every one of the 98 catalogue entries was re-checked against the program, paragraph and line
  it cites; all 98 resolve.
- The workbook contains 22 formulas (`COUNTIF` and `SUM` only). `scripts/recalc.py` could not be
  used because LibreOffice does not function in the build container — it times out even on a
  three-cell workbook. The formula ranges and their expected results were instead verified
  directly against the source data, and `fullCalcOnLoad` is set so Excel recalculates on open.

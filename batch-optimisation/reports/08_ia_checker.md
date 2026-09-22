# IA Checker output - batch tuning artifacts

Produced by the Impact Analysis Checklist v3 automated rules
(`cardlink-change-safety/scripts/ia_check.py`), AFTER-only scan.

---

## Impact Analysis Report

**Detected Language:** JCL
**Member:** PATTERNS
**Before:** (none — AFTER-only scan)
**After:** batch-optimisation/jcl/PATTERNS.jcl
**Lines:** Before=0  After=181
**Diff:** +181 / -0 / ~0

### Diff Summary (key changes)

- Added 181 line(s) at 1: //********************************************************************

### Violations

| Severity | Rule ID | Line | Description | Offending Code |
|---|---|---|---|---|
| — | (none) | — | No violations detected | |

### Summary Counts

- FAIL: 0
- WARN: 0
- INFO: 0
- Rule groups checked: 29

### Recommendation

**GO.** No FAIL or WARN findings from the automated rules.

> Automated rules only. Still work the human-judgment items in the applicable IA v3 sections, and apply the defect-pattern review to every changed paragraph. A clean automated report is not a GO on its own.

---

## Impact Analysis Report

**Detected Language:** JCL
**Member:** JMYBTUNE
**Before:** (none — AFTER-only scan)
**After:** batch-optimisation/jcl/JMYBTUNE.jcl
**Lines:** Before=0  After=100
**Diff:** +100 / -0 / ~0

### Diff Summary (key changes)

- Added 100 line(s) at 1: //JMYBTUNE JOB (ACCT),'MY BATCH TUNE VERIFY',

### Violations

| Severity | Rule ID | Line | Description | Offending Code |
|---|---|---|---|---|
| WARN | GEN-PROD-DSN | 39 | Hardcoded PRD* DSN in a member that uses &ENV — UAT and genbase runs will read/write PRODUCTION datasets. If intentional (shared read-only parm), say so in a comment on the line | `//         JCLLIB ORDER=(PRDCRD.BTHPRC.MY20A2)  PROD MASTER: THE JCL` |
| INFO | JCL-CLASS-CHANGE | 2 | CLASS= changed or added — verify with scheduler/SysAdmin | `//             CLASS=A,` |
| INFO | JCL-COND-CHANGE | 83 | COND= or step-level RC handling changed — verify behaviour with OPC | `//CMPOUT   EXEC PGM=IEBCOMPR,COND=(0,NE,CNTBASE)` |
| INFO | JCL-COND-CHANGE | 94 | COND= or step-level RC handling changed — verify behaviour with OPC | `//LISTJCL  EXEC PGM=IEBPTPCH,COND=EVEN` |

### Summary Counts

- FAIL: 0
- WARN: 1
- INFO: 3
- Rule groups checked: 29

### Recommendation

**GO WITH CONDITIONS.** No FAIL findings. 1 WARN and 3 INFO items — document each exception in CAB, or remediate.

> Automated rules only. Still work the human-judgment items in the applicable IA v3 sections, and apply the defect-pattern review to every changed paragraph. A clean automated report is not a GO on its own.


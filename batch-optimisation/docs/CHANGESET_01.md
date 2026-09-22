# Change set 01 — MY batch tuning, phase 1

Seven line-level changes across four JCL members and three PROCs. All are JCL/PROC/CTL
only: **no COBOL recompile, no genbase, no copybook, no OPC change**, and every one is
allocation, buffering or blocking — none alters record content or sort order.

Evidence: [`../reports/10_longpole_findings.md`](../reports/10_longpole_findings.md).
Verification for all seven: [`../jcl/JMYBTUNE.jcl`](../jcl/JMYBTUNE.jcl) — `IEBCOMPR`
must return RC=00 against the pre-change output.

| # | Member | Library | Change | Risk |
| --- | --- | --- | --- | --- |
| 1 | `JCP1488U` | BTHJCL | `REGION=18M` → `0M` | Low |
| 2 | `JCP1489U` | BTHJCL | `REGION=18M` → `0M` | Low |
| 3 | `JCPAAS09` | BTHJCL | `REGION=18M` → `0M` | Low |
| 4 | `JCP1484U` | BTHJCL | `REGION=17M` → `0M`, fix `OPTION` card | Medium |
| 5 | `CLRNP02` | BTHPRC | STEP040: add `DFSPARM`, fix `BLKSIZE` | Low |
| 6 | `PYMOAAS1` | BTHPRC | 3 × hard-coded `BLKSIZE` → `0` | Low |
| 7 | `CEDCAAS` | BTHPRC | `OADCBF`: add `AMP` buffers | Low |

Not in this change set, and deliberately so: the `CLRNP02` / `CLRNP03` virtual tape
intermediates. That is the largest single lever and it needs a DASD capacity decision
from storage — see §6 of the findings report.

---

## 1–3. Lift `REGION` on `JCP1488U`, `JCP1489U`, `JCPAAS09`

A DFSORT step in an 18 MB region cannot take `MAINSIZE=MAX`, cannot Hipersort and
cannot use memory object sorting. The control member is ignored; the job card wins.

`JCP1488U` and `JCP1489U`, before:

```jcl
// CLASS=A,REGION=18M
```

after:

```jcl
// CLASS=A,REGION=0M               TUNE01 WAS 18M
```

`JCPAAS09`, before:

```jcl
// MSGCLASS=X,REGION=18M,CLASS=A,NOTIFY=&SYSUID
```

after:

```jcl
// MSGCLASS=X,REGION=0M,CLASS=A,NOTIFY=&SYSUID    TUNE01 WAS 18M
```

**Precedent.** `JCQDY760` already carries this exact change, annotated in the member:

```
//* LASTCHANGE MYC2DTA 27/05/2020 CHANGE REGION FROM 17M TO 0M
```

Follow that convention — annotate the line rather than changing it silently, so the
next reader sees the history the same way.

**Watch for.** `REGION=0M` lets a step take what it asks for. If a looping program
previously died on a storage constraint it will now run longer before failing. Confirm
with capacity planning that the initiator class can carry four more unbounded jobs in
the 12am–8am window; that is a conversation, not a blocker.

---

## 4. `JCP1484U` — region and sort estimate

This is the job that ran 5 h 20 m against a 27-minute average.

Job card, before:

```jcl
// REGION=17M,CLASS=A
```

after:

```jcl
// REGION=0M,CLASS=A               TUNE01 WAS 17M
```

Step `S04SORTC` `SYSIN`, before:

```
 OPTION FILSZ=E80000,DYNALLOC=(DISK)
```

after:

```
 OPTION FILSZ=E5000000,DYNALLOC=(DISK,32)
```

Three things are wrong with the original card. `FILSZ=E80000` estimates 80,000
records; DFSORT sizes work allocation and storage from that, so once the MILOG volume
passes it the sort degrades badly. `DYNALLOC=(DISK)` carries no count, so DFSORT takes
its small default instead of the 32 the estate uses elsewhere. And the 17 MB region
capped whatever storage it could have used anyway.

**On the new estimate.** `E5000000` is the value the estate's own `ICPK5000` member
uses. Over-estimating `FILSZ` costs some over-allocated sort work; under-estimating is
what causes the collapse — so raising it is the safe direction, and `FILSZ=E` is an
estimate that DFSORT adjusts rather than an assertion it can abend on.

Set it properly rather than guessing: run `ICETOOL COUNT` over the MILOG input on a
normal night and on the outlier date, then pick the matching `ICPK` member
(`ICPK<nnnn>` scales the estimate — `ICPK1000` is `E1000000`, `ICPK5000` is
`E5000000`). Replace the inline `OPTION` card with `//DFSPARM DD DSN=&CNTLLIB(ICPKnnnn)`
once the volume is known, so this step stops carrying its own private tuning.

---

## 5. `CLRNP02` STEP040 — the untuned sort in the most expensive job

STEP020 and STEP080 of this PROC both carry
`//DFSPARM DD DISP=SHR,DSN=&CNTLLIB(ICPK5000)`. STEP040 carries nothing, and its
`SYSIN` member `CLRS003` is a bare `SORT FIELDS` + `INCLUDE COND` with no `OPTION`
card at all.

Before:

```jcl
//STEP040  EXEC PGM=SORT,COND=(0,NE)
//SYSOUT   DD  SYSOUT=*
//SORTIN   DD  DSN=&ENV.CIS.BTHSEQ.&VER.CPMTH,DISP=SHR
//SORTOUT  DD  DSN=&ENV.CIS.BTHSEQ.&VER.CPMTH.SORTED,
//             DISP=(NEW,CATLG,DELETE),
//             UNIT=DISK,SPACE=(&PRM,(1000,500),RLSE),
//             DCB=(RECFM=FB,LRECL=800,BLKSIZE=)
//SYSIN    DD  DSN=&CNTLLIB(CLRS003),DISP=SHR
```

After:

```jcl
//STEP040  EXEC PGM=SORT,COND=(0,NE)
//DFSPARM  DD  DISP=SHR,DSN=&CNTLLIB(DYNALL64)      TUNE01 ADDED
//SYSOUT   DD  SYSOUT=*
//SORTIN   DD  DSN=&ENV.CIS.BTHSEQ.&VER.CPMTH,DISP=SHR
//SORTOUT  DD  DSN=&ENV.CIS.BTHSEQ.&VER.CPMTH.SORTED,
//             DISP=(NEW,CATLG,DELETE),
//             UNIT=DISK,SPACE=(&PRM,(1000,500),RLSE),
//             DCB=(RECFM=FB,LRECL=800,BLKSIZE=0)   TUNE01 WAS NULL
//SYSIN    DD  DSN=&CNTLLIB(CLRS003),DISP=SHR
```

`BLKSIZE=` with nothing after it requests nothing, so the dataset takes whatever
default applies instead of a system-determined half-track block. `BLKSIZE=0` asks for
the right answer explicitly.

[`../jcl/DYNALL64.ctl`](../jcl/DYNALL64.ctl) is used here rather than an `ICPK` member
because `CPMTH`'s record volume has not been measured. Once it is, switch to the
matching `ICPK` member — a correct `FILSZ` is worth more than extra work datasets.

---

## 6. `PYMOAAS1` — three under-blocked outputs

Three of the four `ETALK` output files carry a hard-coded block size. `PAYMAT3`, in
the same PROC, already shows the correct form.

| Step | LRECL | Before | After | Records per block |
| --- | ---: | --- | --- | --- |
| `PAYMAT1` | 250 | `BLKSIZE=2500` | `BLKSIZE=0` | 10 → ~111 |
| `PAYMAT4` | 1000 | `BLKSIZE=2000` | `BLKSIZE=0` | **2** → ~27 |
| `PAYMAT5` | 400 | `BLKSIZE=4000` | `BLKSIZE=0` | 10 → ~69 |

For example, `PAYMAT4` before:

```jcl
//             DCB=(BLKSIZE=2000,LRECL=1000,RECFM=FB),
```

after:

```jcl
//             DCB=(BLKSIZE=0,LRECL=1000,RECFM=FB),    TUNE01 WAS 2000
```

Records-per-block figures assume a 3390 half-track block of 27,998 bytes; the exact
value is whatever the system determines for the device.

**Output equivalence.** Block size is a physical attribute. The records are unchanged,
and the downstream `PFTPPR1` step transfers records, not blocks, so the file the
Asccend endpoint receives is byte-for-byte identical. `IEBCOMPR TYPORG=PS` compares
records and will return RC=00.

---

## 7. `CEDCAAS` — the one VSAM DD with no buffers

Four of the five VSAM inputs in this PROC are buffer-tuned. `OADCBF` is not.

Before:

```jcl
//OADCBF   DD  DSN=&ENV.EDC.ONLVSM.&VER.OADCBF,DISP=SHR
```

After:

```jcl
//OADCBF   DD  DSN=&ENV.EDC.ONLVSM.&VER.OADCBF,DISP=SHR,
//             AMP=(AMORG,'BUFND=91','BUFNI=34')       TUNE01 ADDED
```

`BUFND=91,BUFNI=34` is the value already used for `AUMERA`, `AUMERB` and `QMMBLC` in
the same PROC — this makes `OADCBF` consistent with its siblings rather than inventing
a number. `OADCBF` is read sequentially by `OADC807` to produce a flat copy, so the
sequential bias is right.

---

## Deployment

Seven members, two libraries. The three-way symmetry check applies — the identical
member list in all three jobs:

| Job | Direction | Members |
| --- | --- | --- |
| Pre-deployment safety copy | `PRDCRD.BTHJCL.MY20A2` → `.FALLBACK`<br>`PRDCRD.BTHPRC.MY20A2` → `.FALLBACK` | `JCP1488U` `JCP1489U` `JCPAAS09` `JCP1484U` / `CLRNP02` `PYMOAAS1` `CEDCAAS` |
| Deployment | `MGRCRD.*` → `PRDCRD.*` | same, plus `DYNALL64` into `PRDCRD.BTHCTL.MY20A2` |
| Fallback | `.FALLBACK` → `PRDCRD.*` | same |

`DYNALL64` is new, so it appears in the deployment and fallback member lists but has
nothing to back up in the pre-deployment copy. Say so explicitly in the Implementation
Plan — a member present in two of three jobs is exactly what the symmetry check hunts
for, and this one is legitimate.

No load module changes, so fallback is a member copy back: well inside the ≤1 hour
commitment on the RFC risk assessment.

**Suggested split.** Items 1–3 and 5–7 are low risk and can travel together. Item 4
should wait for the `ICETOOL COUNT` measurement and go as its own change with its own
UAT cycle, because it is the one where a wrong number changes behaviour rather than
just performance.

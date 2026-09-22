# Change set 02 — `JCP1704U` and `JCP2513U`

Five changes. Four are performance; one is a **defect fix** that has nothing to do with
speed and should be taken whether or not the rest is.

Evidence: [`../reports/11_jcp1704u_jcp2513u.md`](../reports/11_jcp1704u_jcp2513u.md).
Verification: [`../jcl/JMYBTUNE.jcl`](../jcl/JMYBTUNE.jcl) — `IEBCOMPR` RC=00 against the
pre-change outputs.

The `REGION` changes for both members live in
[`CHANGESET_01.md`](CHANGESET_01.md) and are not repeated here.

| # | Member | Change | Class | Worth |
| --- | --- | --- | --- | --- |
| 1 | `JCP1704U` | Collapse the double `CPBPLT` sort into one pass | Structural | **Highest — daily** |
| 2 | `JCP1704U` | `STEP040A`: add `DFSPARM` and `AMP` to the `JOINKEYS` step | DD-level | High — daily |
| 3 | `JCP1704U` | `STEP040C`: add `AMP` to the 3,000-cylinder `REPRO` load | DD-level | High — daily |
| 4 | `JCP2513U` | **Rename the duplicate `CSSUBS1C` step** | **Defect** | Correctness |
| 5 | `JCP2513U` | `AMP` on the eight `REPRO` loads; `ICPK` on the six history sorts | DD-level | Monthly only |

**Sequence these by frequency, not by size.** `JCP1704U` runs 32 times a month for
2,326 minutes; `JCP2513U` ran once for 70. Items 1–3 are worth roughly 33× item 5 per
unit of effort. Item 4 is not a performance item at all.

---

## 1. `JCP1704U` — one pass over `CPBPLT` instead of two

`S020SORT` and `S090SORT` read the same plastic master and sort on the same key. They
differ only in which ORG codes they keep, and the two sets are disjoint. One DFSORT pass
with two `OUTFIL` groups produces both.

Before — two steps, two full reads of `CPBPLT`:

```jcl
//S020SORT EXEC PGM=SORT
//SORTCNTL DD  DISP=SHR,DSN=PRDCRD.BTHCTL.MY20A2(ICPK0250)
//SORTIN   DD  DISP=SHR,DSN=&ENV.CIS.BTHVSM.&VER.CPBPLT
//SORTOUT  DD  DISP=(,CATLG,DELETE),UNIT=DISK,
//             SPACE=(&PRM,(500,250),RLSE),
//             DCB=(RECFM=FB,LRECL=1000,BLKSIZE=27000),
//             DSN=&ENV.CRD.WRKSEQ.&VER.EIS.CPBPLT
//SYSIN    DD  *
  SORT FIELDS=(20,2,PD,A,288,9,PD,A)
  INCLUDE COND=((20,2,PD,EQ,001,OR,20,2,PD,EQ,201),AND,22,2,PD,NE,998)
  RECORD LENGTH=1000,TYPE=F
...
//S090SORT EXEC PGM=SORT
//SORTCNTL DD  DISP=SHR,DSN=PRDCRD.BTHCTL.MY20A2(ICPK0250)
//SORTIN   DD  DISP=SHR,DSN=&ENV.CIS.BTHVSM.&VER.CPBPLT
//SORTOUT  DD  DISP=(,CATLG,DELETE),UNIT=DISK,
//             SPACE=(&PRM,(300,150),RLSE),
//             DCB=(RECFM=FB,LRECL=1000,BLKSIZE=27000),
//             DSN=&ENV.CRD.WRKSEQ.&VER.EIS.CPBPLT.ORG005
//SYSIN    DD  *
  SORT FIELDS=(20,2,PD,A,288,9,PD,A)
  INCLUDE COND=(20,2,PD,EQ,005,AND,22,2,PD,NE,998)
  RECORD LENGTH=1000,TYPE=F
```

After — `S020SORT` produces both files; `S090SORT` is deleted:

```jcl
//S020SORT EXEC PGM=SORT
//SORTCNTL DD  DISP=SHR,DSN=PRDCRD.BTHCTL.MY20A2(ICPK0250)
//SORTIN   DD  DISP=SHR,DSN=&ENV.CIS.BTHVSM.&VER.CPBPLT
//MAIN     DD  DISP=(,CATLG,DELETE),UNIT=DISK,
//             SPACE=(&PRM,(500,250),RLSE),
//             DCB=(RECFM=FB,LRECL=1000,BLKSIZE=27000),
//             DSN=&ENV.CRD.WRKSEQ.&VER.EIS.CPBPLT
//ORG005   DD  DISP=(,CATLG,DELETE),UNIT=DISK,
//             SPACE=(&PRM,(300,150),RLSE),
//             DCB=(RECFM=FB,LRECL=1000,BLKSIZE=27000),
//             DSN=&ENV.CRD.WRKSEQ.&VER.EIS.CPBPLT.ORG005
//SYSIN    DD  *
  SORT FIELDS=(20,2,PD,A,288,9,PD,A)
  INCLUDE COND=((20,2,PD,EQ,001,OR,20,2,PD,EQ,201,OR,
                20,2,PD,EQ,005),AND,22,2,PD,NE,998)
  RECORD LENGTH=1000,TYPE=F
  OUTFIL FNAMES=MAIN,INCLUDE=(20,2,PD,EQ,001,OR,20,2,PD,EQ,201)
  OUTFIL FNAMES=ORG005,INCLUDE=(20,2,PD,EQ,005)
```

**Why the outputs are identical.** The sort key is unchanged, so the order within each
output is unchanged. The step `INCLUDE` is now the union of the two original filters, and
the `22,2,PD,NE,998` condition is common to both so it stays there. Each `OUTFIL` then
applies exactly the ORG test its original step applied. No record reaches an output it
would not have reached before, and none is dropped.

**One real side effect.** `EIS.CPBPLT.ORG005` is now created at `S020SORT` instead of
after `S060EIS`, so it occupies DASD for the middle of the job rather than the end.
`S01FIL06` still deletes it on entry and `S12FIL02` on exit, so nothing else changes —
but note the longer allocation window for storage.

**Check before cutting `S090SORT`.** Confirm no OPC restart instruction, QRG or operator
runbook names that step. If one does, keep `S090SORT` as an `IEFBR14` no-op rather than
deleting it, so restart points stay valid.

---

## 2. `JCP1704U` `STEP040A` — the `JOINKEYS` step has no tuning at all

This step joins two VSAM masters with a 22-field `REFORMAT` into a 3,000-cylinder output.
Its three siblings all point at an `ICPK` member; this one points at nothing, and neither
join input carries buffers.

Before:

```jcl
//STEP040A EXEC PGM=SORT,COND=(0,NE)
//SYSOUT   DD  SYSOUT=*
//SORTJNF1 DD  DISP=SHR,DSN=&ENV.CRD.BTHVSM.&VER.RDM.CUSPLT
//SORTJNF2 DD  DISP=SHR,DSN=&ENV.CIS.BTHVSM.&VER.CPBCRD
```

After:

```jcl
//STEP040A EXEC PGM=SORT,COND=(0,NE)
//DFSPARM  DD  DISP=SHR,DSN=&CNTLLIB(DYNALL64)         TUNE02 ADDED
//SYSOUT   DD  SYSOUT=*
//SORTJNF1 DD  DISP=SHR,DSN=&ENV.CRD.BTHVSM.&VER.RDM.CUSPLT,
//             AMP=('BUFND=91','BUFNI=138')            TUNE02 ADDED
//SORTJNF2 DD  DISP=SHR,DSN=&ENV.CIS.BTHVSM.&VER.CPBCRD,
//             AMP=('BUFND=91','BUFNI=34')             TUNE02 ADDED
```

`BUFND=91,BUFNI=138` is what `S060EIS` already uses for `CUSPLT` in this same job;
`BUFND=91,BUFNI=34` is the estate's value for a large sequentially-read KSDS. Both are
existing numbers rather than invented ones.

`DYNALL64` is used rather than an `ICPK` member because neither join input's record count
has been measured. Measure both with `ICETOOL COUNT` and switch to the matching `ICPK`
member — a correct `FILSZ` matters more on a join than anywhere else, because DFSORT has
to size two inputs.

---

## 3. `JCP1704U` `STEP040C` — a 3,000-cylinder `REPRO` with default buffers

`STEP040B` defines the cluster correctly, with `SPEED` and `CYLINDERS(3000 200)`.
`STEP040C` then loads it unbuffered.

Before:

```jcl
//INDD1    DD  DSN=&ENV.CRD.BTHSEQ.&VER.RDM.CUSPLT.CCRIS,DISP=SHR
//OUTDD1   DD  DSN=&ENV.CRD.BTHVSM.&VER.RDM.CUSPLT.CCRIS,DISP=SHR
```

After:

```jcl
//INDD1    DD  DSN=&ENV.CRD.BTHSEQ.&VER.RDM.CUSPLT.CCRIS,DISP=SHR,
//             DCB=BUFNO=31                            TUNE02 ADDED
//OUTDD1   DD  DSN=&ENV.CRD.BTHVSM.&VER.RDM.CUSPLT.CCRIS,DISP=SHR,
//             AMP=('BUFND=120','BUFNI=4')             TUNE02 ADDED
```

For a sequential KSDS load the data buffers carry the work, so `BUFND` is the number that
matters and `BUFNI` stays small. `BUFNO=31` on the input matches the value this job
already uses on `CPPLTS`.

---

## 4. `JCP2513U` — the duplicate `CSSUBS1C` step name

**This is a correctness fix, not a tuning change, and it should be taken on its own
merits.**

The job names its `CSSUBST` steps `CSSUBS1C`, `CSSUBS1D`, `CSSUBS1E`, `CSSUBS1F`,
`CSSUBS1G` for history files 1–5, then the merchant-posted block at the end of the job
reuses `CSSUBS1C`:

```jcl
//*  CSSUBS1C  DELETE / DEFINE NEW MERCHANT POSTED FILE
//CSSUBS1C EXEC CSSUBST,COND=(0,NE),
//             PARM.SUBST010=('!ENV! !&ENV !VER! !&VER !PRM! !&PRM')
```

After:

```jcl
//*  CSSUBS1H  DELETE / DEFINE NEW MERCHANT POSTED FILE
//CSSUBS1H EXEC CSSUBST,COND=(0,NE),
//             PARM.SUBST010=('!ENV! !&ENV !VER! !&VER !PRM! !&PRM')
```

`CSSUBS1H` continues the existing letter sequence. Update the step comment to match.

**Why it matters.** A duplicate step name makes any step-level `COND=` reference bind to
the first occurrence, and makes restart-at-step ambiguous — an operator restarting this
job at `CSSUBS1C` after an abend in the merchant-posted block can silently re-run the
history-file-1 rebuild instead. Nothing in the current JCL references either step by
name, so the fix is safe today; it is the restart path that is exposed.

**Before changing it**, check whether any OPC restart instruction, QRG or operator
runbook names `CSSUBS1C`. If one does, it needs updating in the same change — that makes
this a T5 (OPC/scheduling) item as well as T1.

---

## 5. `JCP2513U` — buffers on the eight loads, estimates on the six sorts

Lowest priority of the five: this job ran **once** in June. Do it when the same pattern
is being applied elsewhere, not as a change of its own.

**The eight bulk loads.** `IDCAMS3A`, `IDCAMS3B`, `IDCAMS3C`, `IDCAMS3D`, `IDCAMS3E`,
`IDCAMS3F`, `IDCAMS3G` and `QMTMPT04` each `REPRO` a sort output of 1,000–3,000 cylinders
into a freshly defined KSDS with no buffers. Add to each `OUTDD1`:

```jcl
//             AMP=('BUFND=120','BUFNI=4')             TUNE02 ADDED
```

The eight header-record `REPRO` steps (`IDCAMS2A`–`2G`, `QMTMPT03`) copy a single record
and need nothing.

Also confirm the define members `QMDFH01N`–`QMDFH05N`, `QMDFHXPN`, `QMDFHXSN` and
`QMDFMPTN` specify `SPEED` rather than `RECOVERY`. `JCP1704U`'s equivalent define does,
so the convention exists; a `RECOVERY` define preformats every control area before the
load and roughly doubles it.

**The six untuned sorts.** `SORT1C`, `SORT1D`, `SORT1E`, `SORT1F`, `SORT1G` and
`QMTMPT01` point `SORTCNTL` at `DYNALL32`, which sets the work count but gives no size
estimate — while the four smaller cross-reference sorts in the same job get
`ICPK5000`'s `FILSZ=E5000000`. The big sorts should have the estimate, not the small
ones. Measure each `QMU007.QMHSTnn` with `ICETOOL COUNT` and point `DFSPARM` at the
matching `ICPK` member.

---

## Deployment

Items 1–3 touch one member, `JCP1704U`; items 4–5 touch one member, `JCP2513U`. Both are
already in change set 01's member list for the `REGION` change, so **if change set 01 has
not yet deployed, fold these in rather than shipping the same members twice** — two
changes to one member in flight at once is exactly what the clash check exists to catch.

If change set 01 has already gone, these are a separate change with the usual three-way
symmetry over `PRDCRD.BTHJCL.MY20A2` and its `.FALLBACK`. No PROC, no CTL, no load module,
so fallback is a two-member copy back.

Item 4 may pull in an OPC or QRG update, which makes that part T5 as well as T1 — check
before scoping the RFC.

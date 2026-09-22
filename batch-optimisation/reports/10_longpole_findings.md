# Step-level findings — the long poles and the two runaways

Read from the MY source snapshot (`Current/MY = retrofit-mychg-20260919`): the JCL
members in `PRDCRD.BTHJCL.MY20A2`, the PROCs they invoke from
`PRDCRD.BTHPRC.MY20A2`, and the sort control members in `PRDCRD.BTHCTL.MY20A2`.

This closes the gap recorded in §7 of the main document for six of the seven jobs
named there. `RMMDLM01` is still unread — it is not in the MY JCL library under that
name and no A7 operation claims it.

---

## 1. REGION is capped on the jobs that need storage most

| Job | Avg (min) | Job card |
| --- | ---: | --- |
| `JCP1488U` | 74.41 | `REGION=18M` |
| `JCP1489U` | 26.69 | `REGION=18M` |
| `JCPAAS09` | 10.11 (max 145.57) | `REGION=18M` |
| `JCP1484U` | 27.45 (max 319.87) | `REGION=17M` |
| `JCQDY760` | 45.04 | `REGION=0M` |

`JCQDY760` carries this comment in its own JCL:

```
//* LASTCHANGE MYC2DTA 27/05/2020 CHANGE REGION FROM 17M TO 0M
```

So the estate has already made exactly this change once, deliberately, and recorded
it. That is the precedent to cite at CAB.

A DFSORT step in an 18 MB region cannot take `MAINSIZE=MAX`, cannot Hipersort and
cannot use memory object sorting, whatever the control member says. Every other sort
recommendation in this pack is capped by the job card until `REGION` is lifted.

---

## 2. `JCP1488U` / PROC `CLRNP02` — 74 minutes, the longest job on the longest chain

Six working steps. Three of them write an intermediate to **virtual tape**, and two
later steps read those tapes back:

| Step | Program | Writes | Unit |
| --- | --- | --- | --- |
| STEP020 | `SORT` | `&ENV.CIS.BTHSEQ.&VER.MYC.CPADD.NP2.MRG` | **VTAPE1** |
| STEP040 | `SORT` | `&ENV.CIS.BTHSEQ.&VER.CPMTH.SORTED` | DISK |
| STEP060 | `MYCLRNP2` | `&ENV.CIS.BTHSEQ.&VER.MYC.CPADD.NP2` | **VTAPE1** |
| STEP080 | `SORT` | `&ENV.CIS.BTHSEQ.&VER.MYC.CPADD.NP2.SRT` | **VTAPE1** |

STEP060 reads STEP020's tape; STEP080 reads STEP060's tape. That is three virtual
tape writes and two virtual tape reads inside one job, on the critical path.

Two further defects in the same PROC:

- **STEP040 has no `DFSPARM`.** STEP020 and STEP080 both carry
  `//DFSPARM DD DISP=SHR,DSN=&CNTLLIB(ICPK5000)`, which supplies
  `OPTION FILSZ=E5000000,DYNALLOC=(DISK,32)`. STEP040 has neither a size estimate
  nor dynamic allocation, and its `SYSIN` member `CLRS003` is a bare
  `SORT FIELDS` + `INCLUDE COND` with no `OPTION` card. It is the untuned sort in
  the estate's most expensive job.
- **STEP040 codes a null block size:** `DCB=(RECFM=FB,LRECL=800,BLKSIZE=)`. The
  subparameter is empty, so nothing is requested. It should be `BLKSIZE=0` for a
  system-determined half-track block.

The PROC does show the estate tunes VSAM properly when it looks:
`//CPBSYS DD ... AMP=(AMORG,'BUFND=46','BUFNI=3')`.

---

## 3. `JCP1489U` / PROC `CLRNP03` — 26.7 minutes, and it inherits the tape

Four steps, all `IEFBR14` or `IDCAMS`:

- STEP020 `REPRO` copies the `CPADD` KSDS out to `CPADD.BK` on **VTAPE1**.
- STEP040 `REPRO` loads `MYC.CPADD.NP2.SRT` — **the VTAPE1 dataset `CLRNP02`
  STEP080 just wrote** — back into the `CPADD` KSDS.

So the A7#2 chain is tape-bound end to end: `JCP1488U` writes to virtual tape and
`JCP1489U` reads it straight back. Neither `INDD1` nor `OUTDD1` carries an `AMP`
buffer specification on any step, although STEP030 deletes and redefines the KSDS
immediately before the load in STEP040.

---

## 4. `JCPAAS09` / PROCs `CEDCAAS` + `PYMOAAS1` — avg 10 min, worst night 145 min

`CEDCAAS` copies five VSAM files out to sequential. Four of the five VSAM DDs are
buffer-tuned; **one is not**:

| DD | AMP |
| --- | --- |
| `AUSYS` | `BUFND=22, BUFNI=50` |
| `AUMERA` / `AUMERB` | `BUFND=91, BUFNI=34` |
| `OADCTF` | `BUFND=496, BUFNI=13` |
| `QMMBLC` | `BUFND=91, BUFNI=34` |
| **`OADCBF`** | **none** |

`PYMOAAS1` then runs four `ETALK` encryption steps and FTPs the results out. Three
of the four outputs are hard-coded to a small block size:

| Step | LRECL | BLKSIZE coded | Records per block |
| --- | ---: | ---: | ---: |
| `PAYMAT1` | 250 | 2500 | 10 |
| `PAYMAT3` | 2500 | **0** | system determined |
| `PAYMAT4` | 1000 | 2000 | **2** |
| `PAYMAT5` | 400 | 4000 | 10 |

`PAYMAT4` writes two records per block where a half-track 3390 block would hold 27.
`PAYMAT3` already shows the correct form, `BLKSIZE=0`, in the same PROC.

**The likely cause of the 145-minute night is the last step, not the encryption.**
`PYMOAAS1` ends with `//S01FTP EXEC PFTPPR1`, a `PUT` of four files to an external
Asccend endpoint (`cd mfasccend/outbound/WL`). A 14× overrun with a P95 *below* the
average is the shape of one hung or retried transfer, not of gradual growth. Pull the
`PFTPPR1` spool for the outlier date before changing anything in this job.

---

## 5. `JCP1484U` — avg 27 min, worst night 320 min

The root cause is visible in the member. `S04SORTC` sorts an 8,047-byte record with:

```
 OPTION FILSZ=E80000,DYNALLOC=(DISK)
```

Three problems in one card:

1. **`FILSZ=E80000` estimates 80,000 records.** DFSORT sizes its work allocation and
   storage from that estimate. When the MILOG volume exceeds it the sort degrades
   badly — which is exactly a 27-minute job becoming a 320-minute job on one night.
2. **`DYNALLOC=(DISK)` gives no count**, so DFSORT takes its default handful of work
   datasets rather than the 32 that `ICPK5000` asks for elsewhere in the estate.
3. **`REGION=17M`** caps whatever storage DFSORT could otherwise use.

The sort input is also on virtual tape. The member records why:

```
//* 2022-0701 - B810NKP - CHG MILOG.SORT BIG FILE TO VTAPE1
```

and the original DASD allocation is still there, commented out:
`UNIT=DISK,SPACE=(CYL,(1000,0500),RLSE)`. So the file was moved to tape to relieve
DASD, and the sort estimate was never revisited afterwards.

---

## 6. What this changes

The top of the work queue is no longer "add DYNALLOC broadly". It is:

1. Lift `REGION` on the four capped jobs — one-line change, existing precedent.
2. Correct `FILSZ` and `DYNALLOC` on `JCP1484U` STEP `S04SORTC`.
3. Give `CLRNP02` STEP040 a `DFSPARM` and a real `BLKSIZE`.
4. Set `BLKSIZE=0` on the three under-blocked `PYMOAAS1` outputs.
5. Add the missing `AMP` to `CEDCAAS` `OADCBF`.
6. Decide, with storage, whether the `CLRNP02`/`CLRNP03` virtual tape intermediates
   come back to DASD. Largest single lever, and the only one needing a capacity call.

# Patch Validation — CIMB MY Allow Transaction Posting For In-active BIN

**Change:** BIN 45993903 to be treated as on-us and allowed to post while its PCIF prefix
record is in-active
**Patches reviewed:** `MMB00369` (MIPYMT, CCP) · `MCP00850` (CPD030, COB)
**Documents reviewed:** TS v1.0 (CIMB MY/CL/TS/001) · IG v1.0 (CIMB MY/CL/IG/001) ·
FS Sign-Off & Acknowledgement Form (FS v1.1, CIMB MY/CL/FS/001)
**Code baseline:** MY generated user base — `Cardlink Code/extracted_my/extracted_MY_members`
(`MIPYMT.txt`, `CPD030.txt`, `CPS948.txt`, `CPS148.txt`), snapshot June 2026, both patches
confirmed **not yet applied** (`MMB00369`, `MCP00850`, `ALLOW-ON-US-BIN` → 0 hits)

---

## 1. Verdict

| Area | Result |
|---|---|
| Patch text vs TS section 10 | **Exact match**, line-for-line, both patches |
| Patch module types vs IG section 2 | **Match** (MIPYMT = CCP, CPD030 = COB) |
| Sequence-number insertion slots | **All free**, no collisions, correct data levels |
| COBOL syntax / scope integrity | **Valid** in all five insertion sites |
| **MCP00850 (CPD030) functional correctness** | **OK** |
| **MMB00369 (MIPYMT) functional correctness** | **FAILS — unreachable for an in-active BIN** |
| IG fallback section | **Incomplete** — CPD030 batch fallback missing |
| TS section 1.1 scope statement | **Wrong text** — refers to a different change |

The batch half of this change works. The online half does not fire in the scenario the
change exists for, because `CPS948` filters in-active prefix records *before* MIPYMT reaches
the patched line. Detail in section 4.

---

## 2. Patch ↔ TS text comparison

Both patch members reproduce the TS code exactly, including Cardlink sequence numbers and
the patch-ID tag in columns 73-80.

**MCP00850 → TS section 10.2.1.1.** `017902`-`017920` (working storage), `168002`-`168024`
(LI-GMT-LOAD-REC-TYPE-2), `199002`-`199024` (UI-GMT-LOAD-MONETARY-REC). No differences.

**MMB00369 → TS section 10.1.1.1.** `015302`-`015306` (working storage), `043902`-`043910`
(B200-CHECK-ON-US-CARD). No differences.

Header cards agree with IG section 2:

| Patch | Header card | IG section 2 |
|---|---|---|
| MCP00850 | `,,CPD030  EXC UPD  COB 000100` | 2.2.1 CIA — CPD030 (COB) |
| MMB00369 | `,,MIPYMT  EXC UPD  CCP 000100` | 2.1.1 CMBI — MIPYMT (CCP) |

---

## 3. Insertion-point validation against live source

Every slot was checked against the real member. All are unoccupied and the surrounding
data levels match.

### CPD030 (`MCP00850`)

| Slot | Neighbours in source | Verdict |
|---|---|---|
| `017902`-`017920` | `017900*` comment (CX32540) → `017950 01 WS-SORT-RETURN` (CX32540) | Free. `01 WS-ALLOW-BIN` with `03` subordinates matches surrounding `01`/`03` style |
| `168002`-`168024` | `168000 PERFORM SEARCH-POST-ORG-TYPE THRU SPOT-EXIT` → `168050*` → `168100 IF WS-OUTPUT-ORG…` | Free |
| `199002`-`199024` | `199000 PERFORM SEARCH-POST-ORG-TYPE THRU SPOT-EXIT` → `199050*` → `199100 IF WS-OUTPUT-ORG…` | Free |

Scope note: `168000` and `199000` carry **no terminating period** — the insertion lands
inside an enclosing conditional. The patch introduces no period either (it closes with
`END-IF`), so the enclosing scope is preserved. Correct.

Placement is also semantically right: the override runs *after*
`PERFORM SEARCH-POST-ORG-TYPE` has populated `WS-OUTPUT-ORG` / `WS-OUTPUT-TYPE` and
*before* `168100` / `199100` consume them into `CPS316-ORG` / `CPS316-TYPE`. So the forced
`001`/`114` reaches the posting record.

### MIPYMT (`MMB00369`)

| Slot | Neighbours in source | Verdict |
|---|---|---|
| `015302`-`015306` | `015300*` commented-out WS-EXPONENT (V20MB020) → `015400 03 WS-ABSTIME` | Free. `03` level correct for the enclosing group |
| `043902`-`043910` | `043900 IF NOT-ON-US-TXN` → `044000 MOVE '1' TO MIC003-BYTE-MAP-IND (44)` | Free |

Syntax at `043902`: the nested `IF ALLOW-ON-US-BIN` is closed by `END-IF` at `043910`; the
outer `IF NOT-ON-US-TXN` is closed by the period on `044800 GO TO 9888-RETURN-TO-CICS.`
Valid. `GO TO B300-READ-CPSYS` exits the IF to the paragraph at `045000`, which is the
immediately following paragraph — legal, and equivalent to falling through.

### Name-clash check

No pre-existing `WS-ALLOW-*` or `ALLOW-ON-US-BIN` in either member. CPD030 already has
`WS-OUTPUT-ON-US-TYPE` (`168350`, `199350`) — distinct from the patch's
`WS-ALLOW-ON-US-TYPE`. No clash.

---

## 4. BLOCKER — MMB00369 never executes for an in-active BIN

### Evidence

**(1) `CPS148` defines status `'8'` as in-active:**

```cobol
002300      03  CP-STATUS               PIC  X(01).
002400          88  ACTIVE-PREFIX-REC        VALUE '1'.
002500          88  INACTIVE-PREFIX-REC      VALUE '8'.
```

It also confirms the `CR-FLAG` values on the PCIF screen:
`88 CP-FLAG-TYPE VALUE 'T'` / `CP-FLAG-RANGE 'R'` / `CP-FLAG-NTWK 'N'`.

**(2) `CPS948` skips in-active records.** `CIA-CPPFXA-NEXT-REC` is the *only* read-next path
used by the prefix search, and change `MCS00263` added a filter loop to it:

```cobol
010000     IF ((CSCGIO-EIBRESP IS EQUAL DFHRESP(NORMAL))  OR
010005         (CSCGIO-EIBRESP IS EQUAL DFHRESP(DUPKEY))) AND
010010        (INACTIVE-PREFIX-REC)                                     MCS00263
010020         GO TO CIA-CPPFXA-NEXT-REC                                MCS00263
010030     END-IF.
```

So a `CP-STATUS = '8'` record is passed over as if it were not in the file.

**(3) The PCIF sample in TS section 3.1 and IG Appendix A shows `STAT = 8` on _both_
45993903 rows** — the `'T'` row (ORG 001 / TYPE 114) and the `'R'` row (ORG 000 / TYPE 000).

**(4) All three CPS948 search legs therefore fail to match**, because each one obtains its
record through the filtering `CIA-CPPFXA-NEXT-REC`:

- `CIA-CHECK-ORG-TYPE-WITH-CARDNO` (`CP-FLAG-TYPE`) — record skipped, next record is a
  different prefix, range test fails
- `CIA-CHECK-ON-US-WITH-CARDNO` (`CP-FLAG-RANGE`) — same
- `CIA-CHECK-NOT-ONUS-CARD-SCHEME` (`CP-FLAG-NTWK`) — same

Control reaches `CIA-CHECK-NOT-VALD-CARD-SCHEME` → `GO TO CIA-QUAL-REJECT`:

```cobol
017300 CIA-QUAL-REJECT.
017400     MOVE SPACE TO WS-CARD-SCHEME.
017500     MOVE 998   TO WS-CARD-ORG-NMBR
017600                   WS-CARD-TYPE-NMBR.
```

`CIA-QUAL-REJECT` never sets `WS-ON-PREFIX`; it stays `WS-NOT-ON-PREFIX`, set at `002400`
on entry.

**(5) MIPYMT rejects at `043300`, six lines above the patch:**

```cobol
043300     IF  NOT WS-ON-PREFIX                                         V20MB016
043400         MOVE 'U'                TO WS-MIC003-RETURN-CODE         V20MB016
043500         MOVE '1'                TO MIC003-BYTE-MAP-IND(039)      V20MB016
043600         MOVE 912                TO MIC003-B039-ACTION-CODE       V20MB016
043700         GO TO 9000-ERROR-ROUTINE.                                V20MB016
043800*
043900     IF  NOT-ON-US-TXN            ← patch inserted at 043902
```

The MBI payment is declined with action code **912** and control never reaches `043902`.

### When the patch *does* fire

Only when the BIN resolves ON-PREFIX but NOT-ON-US — i.e. matched on the `'N'` network leg,
or matched on the type leg with `CP-SCHEME = 'D'` / `'E'` (`CPS948` `004102`-`004116`). Both
require the prefix record to be **active**. That is the opposite of this change's premise.

### Suggested remedy

Move the MMB00369 logic **above** the `WS-ON-PREFIX` gate — insert in the free range
`043202`-`043298`, testing the BIN off `MIC003-B002-PAN-19` and branching to
`B300-READ-CPSYS`, so it pre-empts both the `043300` and `043900` rejects.

Do **not** fix this by changing `CPS948`. It is a shared CCC copybook; removing the
`MCS00263` filter would change prefix resolution for every consumer and force a re-compile
of the whole dependent list — which IG section 3.4 currently, and correctly, states as N/A.
Keep the fix program-local to MIPYMT.

> Caveat: `CPS948`/`CPS148` were read from the June 2026 MY snapshot. Confirm the production
> MY level of `CPS948` still carries `MCS00263` before finalising. If it does not, this
> blocker does not apply.

---

## 5. Secondary observations

**(a) Card-position guard is asymmetric.** CPD030 guards `(1:3) = '000'` before reading the
BIN at `(4:8)`; MIPYMT does not guard `MIC003-B002-PAN-19(1:3)`. The 19-byte field holds a
16-digit PAN right-aligned with three leading zeros — which is exactly why CPD030 checks it.
For a genuine 19-digit PAN, `(4:8)` is not the BIN, so an unrelated card whose digits 4-11
happen to be `45993903` would be forced on-us. Low likelihood, zero cost to close, and the
two patches should read the same way.

**(b) MIPYMT forces no ORG/TYPE.** CPD030 moves `001`/`114` into `WS-OUTPUT-ORG` /
`WS-OUTPUT-TYPE`. MIPYMT only does `SET ON-US-TXN TO TRUE`, leaving `WS-CARD-ORG-NMBR` /
`WS-CARD-TYPE-NMBR` as CPS948 left them — `998`/`998` on the `CIA-QUAL-REJECT` path, zeroes
on the network path. Neither is `001`/`114`. The patch matches the TS as written, so this is
a **TS-level** gap rather than a patch defect; worth confirming with the author whether the
online path needs the same org/type forcing the batch path gets.

**(c) MIPYMT applies no TC filter.** CPD030 restricts the override to twelve transaction
codes (`2004 2005 2012 2013 2017 2025 2201 2203 4201 4203 4204 6008`). MIPYMT applies it to
every MBI payment for the BIN. Both patch banners say "POSTING FOR CERTIAN TC" [sic]. This
may be deliberate — MIPYMT handles payments only — but it cannot be confirmed from the
material supplied, because **the FS itself was not provided**; only its sign-off form was,
and both TS section 2 and the requirements trace defer to "FS section 2".

**(d) `WS-ALLOW-ON-US-BIN` has no VALUE clause** in either patch. Every test site is
immediately preceded by a `MOVE`, so this is correct as written — just note the field must
never be tested without that MOVE.

---

## 6. Document review

**Traceability.** FS v1.1 signed 21/07/2026 (Mazlan Abd Latif, Director) and 23/07/2026
(Lean Thiam Fatt / Loh Ying Hui, CCPF-BSP CC Issuing, AVP/VP); TS and IG both v1.0 Final,
24/07/2026, author Jin Huei Cheong. Chronology is consistent. PCIF evidence screen dated
14/07/2026.

**Findings.**

1. **TS section 1.1 scope is the wrong text** — "This document describes the technical
   enhancement on Cardlink **SG Block Code K Enhancement**". Copy-paste from another
   document; contradicts section 1.2(a) ("CIMB MY environment only"). Correct before issue.
2. **IG section 8 Fallback is incomplete.** It lists only "Revert change to original online
   (MIPYMT) loads". CPD030 is a batch module — IG section 3.2.4 generates
   `DEVCL2.BTHLOD.MY20A4` for it and section 7.3 copies it to production on Day 2 — so the
   fallback must also cover reverting the CPD030 BTHLOD load. As written, a Day-2 batch
   failure has no documented back-out.
3. **TS and IG "Reviewer 2" approval blocks are blank** in both documents.
4. **FS not supplied.** Only the sign-off form was provided, so requirement-level
   verification (notably the TC list and the MIPYMT/CPD030 asymmetries in 5(b) and 5(c))
   could not be completed.

**Correct as-is.** IG section 2.3 PCT/PPT = N/A (no new transaction or program definition);
IG section 3.4 re-compile list = N/A (no copybook is modified — both patches are
program-local, which the code confirms); IG section 3.3 compile sequence puts CCP (9) before
COB (10), matching the two module types; cutover correctly splits online MIPYMT to Day 1 and
batch CPD030 to Day 2 after the daily batch run.

---

## 7. Actions

| # | Action | Owner | Severity |
|---|---|---|---|
| 1 | Re-position MMB00369 above the `043300` `WS-ON-PREFIX` gate; re-issue TS section 10.1.1.1 | Dev / TS author | **Blocker** |
| 2 | Confirm production MY `CPS948` still carries the `MCS00263` in-active filter | Dev | **Blocker (pre-req)** |
| 3 | Add CPD030 BTHLOD revert to IG section 8 | IG author | High |
| 4 | Confirm from FS whether MIPYMT needs the TC filter and the 001/114 org/type forcing | BA / FS author | High |
| 5 | Add `(1:3) = '000'` guard to MMB00369 for consistency with MCP00850 | Dev | Medium |
| 6 | Fix TS section 1.1 scope text; obtain Reviewer 2 sign-off on TS and IG | TS/IG author | Low |

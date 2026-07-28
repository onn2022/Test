# Patch Validation — CIMB MY Allow Transaction Posting For In-active BIN

**Change:** BIN 45993903 to be treated as on-us and allowed to post while its PCIF prefix
record is in-active
**Patches reviewed:** `MMB00369` (MIPYMT, CCP) · `MCP00850` (CPD030, COB)
**Documents reviewed:** TS v1.0 (CIMB MY/CL/TS/001) · IG v1.0 (CIMB MY/CL/IG/001) ·
FS Sign-Off & Acknowledgement Form (FS v1.1, CIMB MY/CL/FS/001)
**Code baseline:** MY generated user base — `Cardlink Code/extracted_my/extracted_MY_members`
(`MIPYMT.txt`, `CPD030.txt`, `CPS948.txt`, `CPS148.txt`), snapshot June 2026, both patches
confirmed **not yet applied** (`MMB00369`, `MCP00850`, `ALLOW-ON-US-BIN` → 0 hits)
**Empirical evidence:** test region, pre-patch, prefix set to status 8 → MBI payment rejects
with **action code 111**

---

## 1. Verdict

| Area | Result |
|---|---|
| Patch text vs TS section 10 | **Exact match**, line-for-line, both patches |
| Patch module types vs IG section 2 | **Match** (MIPYMT = CCP, CPD030 = COB) |
| Sequence-number insertion slots | **All free**, no collisions, correct data levels |
| COBOL syntax / scope integrity | **Valid** in all five insertion sites |
| MCP00850 (CPD030) functional correctness | **OK** |
| MMB00369 (MIPYMT) functional correctness | **OK — confirmed reachable by the 111 reject** |
| IG fallback section | **Incomplete** — CPD030 batch fallback missing |
| TS section 1.1 scope statement | **Wrong text** — refers to a different change |

Both patches are sound. The remaining items are documentation defects, not code defects.

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

## 4. MMB00369 reachability — confirmed correct by the test-region 111

The pre-patch test result settles this. MIPYMT raises action code **111** at exactly one
place relevant here:

```cobol
043900     IF  NOT-ON-US-TXN                                            V20MB016
044000         MOVE '1'                TO MIC003-BYTE-MAP-IND (44)      V20MB016
044300         MOVE 'NOT ON-US CARD NUMBER         '                    V20MB016
044600         MOVE 111                TO MIC003-B039-ACTION-CODE       V20MB016
044800         GO TO 9888-RETURN-TO-CICS.                               V20MB016
```

(The only other `111` in the member is at `106440`, a CPPLT read `NOTFND` with message
`CARD NOT FOUND` — a different path, and not triggered by a prefix status change.)

Reaching `044600` proves the earlier gate passed:

```cobol
043300     IF  NOT WS-ON-PREFIX  →  action code 912   ← NOT taken
043900     IF  NOT-ON-US-TXN     →  action code 111   ← taken
```

So on a status-8 BIN, CPS948 returns **`WS-ON-PREFIX` = TRUE and `NOT-ON-US-TXN` = TRUE**.
`MMB00369` inserts at `043902`, inside that same taken branch and ahead of the `111` moves —
therefore **the patch executes and suppresses exactly this reject.** It is correctly placed.

### Which CPS948 leg produces that state

`CPS948` sets `WS-ON-PREFIX` TRUE in only three places. Two are ruled out here — the on-us
type match at `004560` (record is inactive, and it would set `ON-US-TXN`, not `NOT-ON-US`)
and the `CP-SCHEME = 'D'/'E'` branch at `004116` (scheme is `'V'`). That leaves
`CIA-CHECK-NOT-ONUS-CARD-SCHEME`, the network leg:

```cobol
005710     SET  CP-FLAG-NTWK            TO TRUE.
005780         IF (CP-FLAG-NTWK) AND …range match…
005840             MOVE CP-SCHEME       TO WS-CARD-SCHEME
005850             MOVE ZEROES          TO WS-CARD-ORG-NMBR
005860                                     WS-CARD-TYPE-NMBR
005910             SET NOT-ON-US-TXN    TO TRUE
005920             SET WS-ON-PREFIX     TO TRUE
```

So an **active `CP-FLAG-NTWK` (`'N'`) network-range record still covers this card range**.
It is a separate PCIF entry from the two 45993903 `'T'` and `'R'` records — consistent with
the evidence screen being `PAGE 002 OF 003` — and CIMB's status change did not touch it.
The `'T'` and `'R'` records are skipped as in-active by `CIA-CPPFXA-NEXT-REC`
(change `MCS00263`, filtering `INACTIVE-PREFIX-REC`, `CP-STATUS '8'` per `CPS148`), the
network record then matches, and MIPYMT lands on the 111.

> **Correction.** An earlier revision of this report claimed the patch was unreachable
> because all three CPS948 legs would miss and fall to `CIA-QUAL-REJECT`, producing a 912.
> That overlooked the active network-range record, which is not shown on the PCIF page in
> the TS/IG. The observed 111 disproves it. No change is required to MMB00369's placement.

### Consequence for org/type — no action needed

On the network leg CPS948 leaves `WS-CARD-ORG-NMBR` / `WS-CARD-TYPE-NMBR` at **zeroes**
(`005850`-`005860`), and the patch does not force `001`/`114` the way CPD030 does. This is
harmless, and the TS asymmetry is deliberate:

- `WS-CARD-ORG-NMBR`, `WS-CARD-TYPE-NMBR` and `WS-CARD-SCHEME` appear **nowhere** in
  MIPYMT — they are referenced only inside the CPS948 copybook. MIPYMT never consumes them.
- MIPYMT keys the plastic read purely on the card number:
  `103710 MOVE MIC003-B002-PAN-19 TO PLASTIC-CARD-NMBR`, then
  `105500 MOVE PLASTIC-KEY TO CSCGIO-REC-KEY`. Org/type do not participate in the key.
- CPD030 by contrast *does* consume `WS-OUTPUT-ORG`/`TYPE` into `CPS316-ORG`/`CPS316-TYPE`
  at `168200`/`199200`, which is why it must force them.

---

## 5. Secondary observations

**(a) Card-position guard is asymmetric — minor.** CPD030 guards `(1:3) = '000'` before
reading the BIN at `(4:8)`; MIPYMT does not guard `MIC003-B002-PAN-19(1:3)`. The 19-byte
field holds a 16-digit PAN right-aligned with three leading zeros, which is why CPD030
checks it. For a genuine 19-digit PAN, `(4:8)` is not the BIN, so an unrelated card whose
digits 4-11 happen to be `45993903` would be forced on-us. Low likelihood, zero cost to
close, and the two patches would then read the same way.

**(b) MIPYMT applies no TC filter.** CPD030 restricts the override to twelve transaction
codes (`2004 2005 2012 2013 2017 2025 2201 2203 4201 4203 4204 6008`). MIPYMT applies it to
every MBI payment for the BIN. Both patch banners say "POSTING FOR CERTIAN TC" [sic]. This
is plausibly deliberate — MIPYMT handles payments only, so the TC is implicit — but it
cannot be confirmed from the material supplied, because **the FS itself was not provided**;
only its sign-off form was, and TS section 2 defers to "FS section 2".

**(c) `WS-ALLOW-ON-US-BIN` has no VALUE clause** in either patch. Every test site is
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
   verification (notably the TC list behind item 5(b)) could not be completed.

**Correct as-is.** IG section 2.3 PCT/PPT = N/A (no new transaction or program definition);
IG section 3.4 re-compile list = N/A (no copybook is modified — both patches are
program-local, which the code confirms); IG section 3.3 compile sequence puts CCP (9) before
COB (10), matching the two module types; cutover correctly splits online MIPYMT to Day 1 and
batch CPD030 to Day 2 after the daily batch run.

---

## 7. Actions

| # | Action | Owner | Severity |
|---|---|---|---|
| 1 | Add CPD030 BTHLOD revert to IG section 8 | IG author | High |
| 2 | Confirm from FS whether MIPYMT is intended to be TC-filtered | BA / FS author | Medium |
| 3 | Consider adding `(1:3) = '000'` guard to MMB00369 for consistency with MCP00850 | Dev | Low |
| 4 | Fix TS section 1.1 scope text; obtain Reviewer 2 sign-off on TS and IG | TS/IG author | Low |

**Regression test to keep.** Re-run the status-8 payment case after the patch: the same
transaction that returns action code 111 pre-patch must post successfully post-patch. That
single case exercises the whole MMB00369 path.

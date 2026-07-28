# Patch Validation — CIMB MY Allow Transaction Posting For In-active BIN

**Change:** BIN 45993903 to be treated as on-us and allowed to post while its PCIF prefix
record is in-active
**Patches reviewed:** `MMB00369` (MIPYMT, CCP) · `MCP00850` (CPD030, COB)
**Documents reviewed:** TS v1.0 (CIMB MY/CL/TS/001) · IG v1.0 (CIMB MY/CL/IG/001) ·
FS Sign-Off & Acknowledgement Form (FS v1.1, CIMB MY/CL/FS/001)
**Code baseline:** MY generated user base — `Cardlink Code/extracted_my/extracted_MY_members`
(`MIPYMT.txt`, `CPD030.txt`, `CPS948.txt`, `CPS148.txt`, `AUSBLKS.txt`), snapshot June 2026.
Both patches confirmed **not yet applied** (`MMB00369`, `MCP00850`, `ALLOW-ON-US-BIN` → 0 hits)
**Empirical evidence:** test region, pre-patch, prefix at status 8 → MBI payment rejects with
**action code 111**

---

## 1. Verdict

| Area | Result |
|---|---|
| Patch text vs TS section 10 | **Exact match**, line-for-line, both patches |
| Patch module types vs IG section 2 | **Match** (MIPYMT = CCP, CPD030 = COB) |
| Insertion slots — free, correct levels, scope intact | **Pass**, all five sites |
| Patch coverage of all affected paths | **Complete** — both `SEARCH-POST-ORG-TYPE` callers patched |
| MMB00369 reachability | **Confirmed** by the 111 reject |
| MCP00850 reachability | **Depends on open item A** — unresolved |
| Side-effect safety of the three `SET`s | **Depends on open item B** — unresolved |
| IG fallback section | **Incomplete** — CPD030 batch fallback missing |
| TS section 1.1 scope statement | **Wrong text** |

Two open items (section 6) need one copybook each. Everything else is verified against source.

---

## 2. Patch ↔ TS text comparison

Both patch members reproduce the TS code exactly, including Cardlink sequence numbers and the
patch-ID tag in columns 73-80.

**MCP00850 → TS 10.2.1.1** — `017902`-`017920` (WS), `168002`-`168024` (LI-GMT-LOAD-REC-TYPE-2),
`199002`-`199024` (UI-GMT-LOAD-MONETARY-REC). No differences.

**MMB00369 → TS 10.1.1.1** — `015302`-`015306` (WS), `043902`-`043910`
(B200-CHECK-ON-US-CARD). No differences.

Header cards agree with IG section 2: `,,CPD030 EXC UPD COB` ↔ CIA/CPD030 (COB);
`,,MIPYMT EXC UPD CCP` ↔ CMBI/MIPYMT (CCP).

---

## 3. Insertion points — verified against live source

| Patch | Slot | Neighbours | Verdict |
|---|---|---|---|
| MCP00850 | `017902`-`017920` | `017900*` → `017950 01 WS-SORT-RETURN` | Free. `01 WS-ALLOW-BIN` is a clean 01-level insert, no group nesting |
| MCP00850 | `168002`-`168024` | `168000 PERFORM SEARCH-POST-ORG-TYPE` → `168050*` → `168100 IF WS-OUTPUT-ORG…` | Free |
| MCP00850 | `199002`-`199024` | `199000 PERFORM SEARCH-POST-ORG-TYPE` → `199050*` → `199100 IF WS-OUTPUT-ORG…` | Free |
| MMB00369 | `015302`-`015306` | `015300*` (commented WS-EXPONENT) → `015400 03 WS-ABSTIME` | Free |
| MMB00369 | `043902`-`043910` | `043900 IF NOT-ON-US-TXN` → `044000 MOVE '1' TO …IND (44)` | Free |

**Scope integrity (CPD030).** `168000`/`199000` carry no terminating period — the insertion
lands inside an enclosing conditional. The patch introduces no period either, closing with
`END-IF`. Enclosing scope preserved.

**Group integrity (MIPYMT).** The `03` at `015302` sits under `01 WS-WORK-FIELDS` (`010500`).
It correctly terminates the preceding `03 WS-CONSOLE-MESSAGE-LINE` group, whose last
subordinate is a `05 … REDEFINES` at `015000`. The new `03` is not itself a REDEFINES and does
not land inside one, and there is no `OCCURS` in scope. Legal.

**Syntax (MIPYMT).** Nested `IF ALLOW-ON-US-BIN` closed by `END-IF` at `043910`; outer
`IF NOT-ON-US-TXN` closed by the period on `044800 GO TO 9888-RETURN-TO-CICS.`
`GO TO B300-READ-CPSYS` targets `045000`, the immediately following paragraph — it skips only
the reject block, which is the intent.

**Name clashes.** No pre-existing `WS-ALLOW-*` or `ALLOW-ON-US-BIN` in either member.
CPD030's existing `WS-OUTPUT-ON-US-TYPE` (`168350`, `199350`) is distinct from the patch's
`WS-ALLOW-ON-US-TYPE`.

---

## 4. MCP00850 — control-flow analysis

Both patch sites sit inside the third branch of an identical three-way conditional. Site 1
(TF1 / record type 2) shown; site 2 (UI / monetary, `197942`-`199380`) is an exact structural
mirror.

```cobol
166940     IF CPS316-TC-TYPE EQUAL TO 6900
166970         MOVE CPS317-HDR-ORG TO CPS316-ORG  WS-GOT-ORG     ← no prefix search
167010     ELSE
167020     IF  CPS317-HDR-POSTING-IND IS EQUAL 'Y'
167040         MOVE TF1-T-ORG      TO CPS316-ORG                 ← no prefix search
167050         MOVE TF1-T-TYPE     TO CPS316-TYPE
167090     ELSE
167100         MOVE TF1-T-CARD-NBR TO WS-PLTCARD-X
167300         PERFORM SHIFT-CARD-LEFT-19 THRU SCL-19-EXIT
168000         PERFORM SEARCH-POST-ORG-TYPE THRU SPOT-EXIT
           ←   PATCH 168002-168024
168100         IF WS-OUTPUT-ORG > ZEROES AND WS-OUTPUT-TYPE > ZEROES
168200             MOVE WS-OUTPUT-ORG  TO CPS316-ORG  WS-GOT-ORG
168250             MOVE WS-OUTPUT-TYPE TO CPS316-TYPE WS-GOT-TYPE
168270         END-IF
168300         MOVE WS-OUTPUT-TXN-IND    TO WS-TXN-IND
168350         MOVE WS-OUTPUT-ON-US-TYPE TO WS-ON-US-TYPE
168370         MOVE TF1-T-CARD-NBR TO CPS316-CARDHLD-NBR
168380     END-IF.
```

**Coverage is complete and correctly scoped.** `SEARCH-POST-ORG-TYPE` is performed in exactly
two places in the entire 17,362-line program — `168000` and `199000` — and both are patched.
The other record-type routines (`LI-GMT-LOAD-REC-TYPE-3` through `-7`,
`UI-GMT-LOAD-AIRLINE-REC`, `UI-GMT-LOAD-INTCHG-DATA`) do not resolve org/type by prefix search,
so an in-active BIN cannot break them. The two bypass branches above take org/type from the
batch header or from the transaction record directly and likewise never consult the prefix
file. Nothing is missed.

**Placement is right.** The override runs after `SEARCH-POST-ORG-TYPE` populates the
`WS-OUTPUT-*` fields and before `168100`/`199100` consume them into `CPS316-ORG`/`CPS316-TYPE`,
so the forced 001/114 reaches the posting record.

**The three `SET`s are load-bearing.** Lines `168300`/`168350` unconditionally copy
`WS-OUTPUT-TXN-IND` and `WS-OUTPUT-ON-US-TYPE` into `WS-TXN-IND` and `WS-ON-US-TYPE`
*after* the patched block. The patch's `SET WS-OUTPUT-ON-US / WS-OUTPUT-VISA /
WS-OUTPUT-VISA-CARD TO TRUE` are what steer those two moves. This is coherent design — but see
open item B.

---

## 5. MMB00369 — confirmed reachable

Action code 111 is raised at exactly one relevant place:

```cobol
043900     IF  NOT-ON-US-TXN
044300         MOVE 'NOT ON-US CARD NUMBER         '
044600         MOVE 111 TO MIC003-B039-ACTION-CODE
044800         GO TO 9888-RETURN-TO-CICS.
```

(The only other `111`, at `106440`, is a CPPLT `NOTFND` / `CARD NOT FOUND` — a different path,
not triggered by a prefix status change.)

Hitting `044600` proves the earlier gate passed — `043300 IF NOT WS-ON-PREFIX` → 912 was **not**
taken. So CPS948 returns `WS-ON-PREFIX` TRUE with `NOT-ON-US-TXN` TRUE, and the patch at
`043902` sits inside that taken branch, ahead of the 111 moves. It executes and suppresses the
reject.

**Which CPS948 leg.** Of the three places CPS948 sets `WS-ON-PREFIX` TRUE, the on-us type match
(`004560`) and the `CP-SCHEME 'D'/'E'` branch (`004116`) are ruled out — the 45993903 `'T'` and
`'R'` records are skipped as in-active by `CIA-CPPFXA-NEXT-REC` (change `MCS00263`, filtering
`INACTIVE-PREFIX-REC` = `CP-STATUS '8'` per CPS148), and the scheme is `'V'`. That leaves
`CIA-CHECK-NOT-ONUS-CARD-SCHEME` (`005910`/`005920`) — an **active `CP-FLAG-NTWK` ('N')
network-range record** still covering the range. It is a separate PCIF entry from the two
45993903 records, not shown on the page reproduced in the TS/IG (`PAGE 002 OF 003`), and
untouched by the status change.

> **Correction.** An earlier revision claimed this patch was unreachable, reasoning that all
> three CPS948 legs would miss and fall to `CIA-QUAL-REJECT` for a 912. That overlooked the
> active network-range record. The observed 111 disproves it. Placement needs no change.

**No org/type forcing needed here.** On the network leg CPS948 leaves `WS-CARD-ORG-NMBR` /
`WS-CARD-TYPE-NMBR` at zeroes (`005850`), and unlike CPD030 the patch does not force 001/114.
That is harmless: `WS-CARD-ORG-NMBR`, `WS-CARD-TYPE-NMBR` and `WS-CARD-SCHEME` appear **nowhere**
in MIPYMT — they are referenced only inside the CPS948 copybook — and MIPYMT keys the plastic
read on the card number alone (`103710 MOVE MIC003-B002-PAN-19 TO PLASTIC-CARD-NMBR` →
`105500 MOVE PLASTIC-KEY TO CSCGIO-REC-KEY`). CPD030 *does* feed `CPS316-ORG`/`TYPE`, which is
why only it needs the forcing. The TS asymmetry is deliberate.

---

## 6. Open items

### A. `TF1-T-CARD-NBR` / `UI-T-CARDHLD-NBR` field length — gates MCP00850 entirely

The `(1:3) = '000'` guard is true **only** if these are 19-byte fields holding a 16-digit PAN
right-aligned with three leading zeros. If they are 16-byte, `(1:3)` is `'459'` for this BIN,
the condition never holds, and **MCP00850 is dead code**.

Evidence it is 19:

- `244650` / `532100`: `MOVE CPS316-CARDHLD-NBR TO WS-CPS316-CARDHLD-NBR`, target
  `PIC 9(16)` (CP1EH049). A numeric move truncating three high-order digits — meaningful only
  if the source carries 19.
- The author wrote the `'000'` test deliberately; it is inert on a 16-byte field.
- MIPYMT's counterpart is explicitly 19 (`MIC003-B002-PAN-19`), and PCIF ranges are 19 digits
  (`0004599390300000000`).

Evidence to be careful:

- `167300` / `198300` run `SHIFT-CARD-LEFT-19` on these very fields, a routine that exists to
  normalise a card into 19-byte zero-padded form — implying the raw field is not assumed to be
  in that form already.
- CPD030 contains **no** existing reference modification on any card field, so there is no
  in-program precedent to lean on.

Not resolvable from CPD030 alone — needs the TF1/UI record copybook. I am flagging rather than
assuming, because this is the exact mirror of the MIPYMT error corrected in section 5.

**Check:** find `TF1-T-CARD-NBR` and `UI-T-CARDHLD-NBR` in their copybook; confirm `PIC X(19)`
or `9(19)`.

### B. Do `WS-OUTPUT-ON-US`, `WS-OUTPUT-VISA`, `WS-OUTPUT-VISA-CARD` share a field?

The patch issues three `SET … TO TRUE` in sequence. If any two are 88-levels on the **same**
underlying item, the later silently overrides the earlier — patch order is ON-US, VISA,
VISA-CARD. Because `168300`/`168350` then copy `WS-OUTPUT-TXN-IND` and `WS-OUTPUT-ON-US-TYPE`
into `WS-TXN-IND` / `WS-ON-US-TYPE`, a collision would land the wrong value on the posted
transaction rather than failing loudly.

The unpatched branches `MOVE 4 TO WS-ON-US-TYPE` (`167000`, `167080`), so
`WS-OUTPUT-ON-US-TYPE` is a small numeric with discrete values — exactly the shape where
`WS-OUTPUT-ON-US` and `WS-OUTPUT-VISA-CARD` could collide.

**Check:** in the copybook behind `COPY CPS548` (`781600`), confirm the three condition names
resolve to at least two distinct parents, and that the resulting `WS-ON-US-TYPE` / `WS-TXN-IND`
values are the intended ones for an on-us Visa posting.

---

## 7. Secondary observations

**(a) MIPYMT has no `(1:3)` guard.** Its field is genuinely 19 (`MIC003-B002-PAN-19`), so
`(4:8)` is correct for a 16-digit PAN — but for a true 19-digit PAN `(4:8)` is not the BIN, and
an unrelated card whose digits 4-11 are `45993903` would be forced on-us. Low likelihood, zero
cost to close, and it would make the two patches read alike.

**(b) MIPYMT applies no TC filter.** CPD030 restricts to twelve TCs
(`2004 2005 2012 2013 2017 2025 2201 2203 4201 4203 4204 6008`); MIPYMT applies the override to
every MBI payment for the BIN. Plausibly deliberate — MIPYMT handles payments only — but
unverifiable here because **the FS itself was not supplied**, only its sign-off form, and TS
section 2 defers to "FS section 2".

**(c) TC field width is consistent.** The patch moves `TF1-T-CODE`/`UI-T-CODE` into
`WS-ALLOW-TC-CODE PIC 9(04)`, matching existing 4-digit TC usage (`CPS316-TC-TYPE EQUAL TO
6900`). An 88 test on a `PIC 9(04)` DISPLAY item compiles to a zoned compare — no S0C7 exposure
even on non-numeric content.

**(d) `WS-ALLOW-ON-US-BIN` has no VALUE clause** in either patch. Every test site is immediately
preceded by a `MOVE`, so this is correct as written — the field must never be tested without it.

---

## 8. Document review

**Traceability.** FS v1.1 signed 21/07/2026 (Mazlan Abd Latif, Director) and 23/07/2026 (Lean
Thiam Fatt / Loh Ying Hui, CCPF-BSP CC Issuing, AVP/VP); TS and IG both v1.0 Final 24/07/2026,
author Jin Huei Cheong. Chronology consistent; PCIF evidence screen dated 14/07/2026.

1. **TS section 1.1 scope is the wrong text** — "the technical enhancement on Cardlink **SG
   Block Code K Enhancement**". Contradicts 1.2(a) ("CIMB MY environment only").
2. **IG section 8 Fallback is incomplete** — lists only the MIPYMT online revert. CPD030 is a
   batch module: IG 3.2.4 generates `DEVCL2.BTHLOD.MY20A4` for it and 7.3 copies it to
   production on Day 2, so a Day-2 batch failure has no documented back-out.
3. **Reviewer 2 approval blocks are blank** in both TS and IG.
4. **FS not supplied** — only the sign-off form, so requirement-level verification of 7(b) could
   not be completed.

**Correct as-is.** IG 2.3 PCT/PPT = N/A; IG 3.4 re-compile list = N/A (no copybook modified —
confirmed, both patches are program-local); IG 3.3 compile sequence puts CCP (9) before COB
(10); cutover correctly splits online MIPYMT to Day 1 and batch CPD030 to Day 2.

---

## 9. Actions

| # | Action | Owner | Severity |
|---|---|---|---|
| 1 | Confirm `TF1-T-CARD-NBR` / `UI-T-CARDHLD-NBR` are 19-byte (open item A) | Dev | **Blocking for CPD030** |
| 2 | Confirm the three `WS-OUTPUT-*` 88s don't share a parent (open item B) | Dev | **High** |
| 3 | Add CPD030 BTHLOD revert to IG section 8 | IG author | High |
| 4 | Confirm from FS whether MIPYMT should be TC-filtered | BA / FS author | Medium |
| 5 | Add `(1:3) = '000'` guard to MMB00369 for consistency | Dev | Low |
| 6 | Fix TS 1.1 scope text; obtain Reviewer 2 sign-off | TS/IG author | Low |

**Regression test.** The status-8 payment that returns action code 111 pre-patch must post
post-patch — one case exercising the whole MMB00369 path. For MCP00850, post a TC 2004 (and one
non-listed TC, to prove the filter) on a 45993903 card through both the type-2 and
user-input paths, and confirm the posting lands on ORG 001 / TYPE 114.

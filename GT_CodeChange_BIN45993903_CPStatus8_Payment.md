# GT Code Change Request: BIN 45993903 — Allow Payment When CP-STATUS = '8'

**Change Reference:** GT-CPX-STATUS8  
**Date:** 2026-07-01  
**BIN Affected:** 45993903 (VISA, ORG=001, TYPE=114)  
**Trigger:** PCIF CP-STATUS to be changed from '1' (Active) to '8' (Inactive/Soft-Disable)

---

## Background

BIN 45993903 has 3 live regular accounts that must continue to accept payments after the prefix
record's CP-STATUS is set to '8'. The PCIF record will NOT be deleted — only the status byte
changes. Bulk Upgrade and CLI/CLD batch operations (CP617180) are expected to skip this BIN, which
is the desired behaviour. The concern is online and authorisation programs that explicitly test
CP-STATUS='1' (condition name CP-ACTIVE) after the CPPFXA/CPS948 prefix lookup.

### CPS948 is already status-blind
The card prefix search routine (CPS948 / CIA-CARD-PREFIX-SEARCH) performs ONLY range matching —
it checks DFHRESP(NORMAL/DUPKEY), CP-FLAG-TYPE, and card number within CP-CARD-RANGE-FROM /
CP-CARD-RANGE-TO. There is NO CP-STATUS check anywhere in CPS948. After a successful match it
sets WS-ON-PREFIX TRUE and exits. Any downstream code that then additionally tests CP-ACTIVE
is what must be changed.

---

## Programs to Change

### Priority 1 — CONFIRMED must investigate

| Program   | Reason for suspicion |
|-----------|----------------------|
| CPOPCTF1  | Found in `CP-ACTIVE AND CPS948` search AND `CP-INACTIVE` also present — has own CP-ACTIVE check outside CPS948 copy expansion |
| AULAUAC   | Authorization V2 Account Verification — uses CPS948; CP-ACTIVE/CP-STATUS present via CPS148 COPY; procedure division check unconfirmed but critical payment path |
| AULAMSM   | Authorization V2 Mastercard Systems Functions — reads CPPFXA directly via GETMAIN (change AM2301) and was found in `CP-ACTIVE AND CP-STATUS AND CPPFXA` search |

### Priority 2 — Lower risk (confirm only)

| Program   | Reason |
|-----------|--------|
| CPLPCLT   | Business Logic for Account Locate — uses WS-GETMAIN-CPPFX flag; may check CP-STATUS after read |
| CPOPCTF2 / CPOPCTF3 | If sister programs of CPOPCTF1 exist for similar card file maintenance flows, apply same check |

### Confirmed NO change required

| Program          | Reason |
|------------------|--------|
| CPS948           | No CP-STATUS check — status-blind range match only |
| MICCSA / MICCAV / MICCMC / MIVUCP / MICCOP | MBI programs — all call CPS948 which is status-blind; no own status check |
| CPCPTB / CPCPTB2 | Batch prefix table loader — no CP-ACTIVE filter confirmed by search |
| CP617180         | SKIP status-8 is correct/expected for Bulk Upgrade |

---

## How to Find the Lines to Change

Open each Priority 1 program in your source editor. Search (F3 / ISPF FIND) for:

```
FIND CP-ACTIVE
```

Examine every occurrence:
- **In DATA DIVISION / COPY statements**: No change needed. These are just the 88-level condition
  definitions coming from COPY CPS148 (via COPY CPS948).
- **In PROCEDURE DIVISION, after a CPS948 call or CPPFXA read**: This IS the gate that must change.

Typical patterns that require change:

**Pattern A — Test after CPS948 call (CPOPCTF1, AULAUAC)**
```cobol
           PERFORM CIA-CARD-PREFIX-SEARCH
           IF WS-ON-PREFIX
              IF CP-ACTIVE                      ← LINE TO CHANGE
                 ...proceed with payment...
              ELSE
                 ...reject / error handling...
              END-IF
           END-IF
```

**Pattern B — Test after direct CPPFXA read (AULAMSM)**
```cobol
           EXEC CICS READ FILE('CPPFXA')
               INTO(WS-CARD-PREFIX-AREA)
               ...
           END-EXEC
           IF DFHRESP(NORMAL)
              IF CP-ACTIVE                      ← LINE TO CHANGE
                 ...proceed...
              END-IF
           END-IF
```

---

## Code Change — Before and After

### Change A: Extend CP-ACTIVE test to also accept CP-STATUS = '8'

**BEFORE:**
```cobol
              IF CP-ACTIVE
```

**AFTER:**
```cobol
              IF CP-ACTIVE OR CP-INACTIVE
```

**Why `CP-INACTIVE`?** — CPS148 defines:
```cobol
      05 CP-STATUS          PIC X(01).
         88 CP-ACTIVE       VALUE '1'.
         88 CP-INACTIVE     VALUE '8'.
```
`CP-INACTIVE` is VALUE '8'. Using the 88-level name is more readable and avoids a hard-coded
literal. The condition `CP-ACTIVE OR CP-INACTIVE` means "either normally active or soft-disabled
— proceed with transaction processing in both cases."

### Change B: If the program rejects on `NOT CP-ACTIVE`

**BEFORE:**
```cobol
              IF NOT CP-ACTIVE
                 MOVE 'PREFIX INACTIVE' TO ...
                 PERFORM ERROR-ROUTINE
              END-IF
```

**AFTER:**
```cobol
              IF NOT (CP-ACTIVE OR CP-INACTIVE)
                 MOVE 'PREFIX INACTIVE' TO ...
                 PERFORM ERROR-ROUTINE
              END-IF
```

### Change C: If the program uses a literal comparison

**BEFORE:**
```cobol
              IF CP-STATUS = '1'
```

**AFTER:**
```cobol
              IF CP-STATUS = '1' OR CP-STATUS = '8'
```

---

## AULAMSM — Specific Context

AULAMSM (Authorization V2 Mastercard Systems Functions) was introduced via change AM2301 to read
CPPFXA directly using GETMAIN rather than going through CPS948. The working storage flags:

```cobol
      03 WS-GETMAIN-CPPFXA-FLAG  PIC X(01) VALUE 'N'.  AM2301
         88 WS-CPPFXA-ALLOCATED  VALUE 'Y'.             AM2301
         88 WS-CPPFXA-NOT-ALLOCATED VALUE 'N'.          AM2301
      03 WS-PREFIX-LEN           PIC 9(02).             AM2301
```

The GETMAIN pattern allocates CPPFXA storage, reads the record, then tests the status. In the
procedure division, find the block introduced by AM2301 that reads CPPFXA and check whether it
subsequently tests CP-ACTIVE. Apply Change A or B above at that point.

---

## CPOPCTF1 — Specific Context

CPOPCTF1 (V20CP070) is the online card transaction file maintenance program (plastic operations).
It sets WS-NEXT-PROGRAM to OAS021B (Mastercard) or OAS021C (Visa) depending on card scheme. The
WS-OLD-CARD-SCHEME / WS-OLD-CARD-TYPE-NMBR fields (change CP2361) suggest it also reads the
OLD card's prefix to validate a card scheme change. There may be TWO places to change:

1. The initial card prefix lookup for the new card number.
2. The old card prefix lookup during a card reissue/upgrade flow.

Search for ALL occurrences of `CP-ACTIVE` in the procedure division of CPOPCTF1 and apply the
change at each point where the status is tested as a payment/processing gate.

---

## Testing After Change

After applying the code changes, compile and test the following scenarios with a card on BIN 45993903
while CP-STATUS = '8' in the PCIF:

1. **Online card payment** — customer performs a purchase; verify transaction completes.
2. **CPOPCTF1 online card maintenance** — perform a block-code update on a BIN 45993903 card.
3. **Authorization flow** — submit an authorisation request for BIN 45993903; verify AULAUAC/AULAMSM
   do not reject with a prefix-inactive error.
4. **Confirm CP617180 still skips** — run a Bulk CLI/CLD test job and confirm BIN 45993903 cards
   are NOT processed (this is expected and should remain unchanged).

---

## CPS148 Copybook — No Change Required

The CPS148 copybook already defines both conditions:
```cobol
      05 CP-STATUS          PIC X(01).
         88 CP-ACTIVE       VALUE '1'.
         88 CP-INACTIVE     VALUE '8'.
```
No change to CPS148 is needed. The fix is in the calling programs' procedure divisions only.

---

## CPOPCMF Screen — Separate Change (Optional)

The CPOPCMF maintenance screen cannot display or accept CP-STATUS because the MAP-CARD-STI
field was commented out in change CP3345P:

```cobol
***    07 MAP-CARD-STL  PIC S9(4) COMP.  CP3345P
***    07 MAP-CARD-STA  PIC X.           CP3345P
***    07 MAP-CARD-STI  PIC X.           CP3345P
```

To change BIN 45993903 CP-STATUS to '8', use **CEBR or File-AID** to directly update the
VSAM KSDS record rather than going through the CPOPCMF screen. If ongoing operational need exists
to set CP-STATUS via screen, raise a separate change to reinstate MAP-CARD-STI in the CPPCMF BMS
map and corresponding CPOPCMF procedure logic.

---

## Summary

| Action | Program | Type | Priority |
|--------|---------|------|----------|
| Find and change `IF CP-ACTIVE` in procedure division | CPOPCTF1 | Online CICS | HIGH |
| Find and change `IF CP-ACTIVE` after CPS948 | AULAUAC | Auth V2 | HIGH |
| Find and change `IF CP-ACTIVE` after CPPFXA GETMAIN | AULAMSM | Auth V2 | HIGH |
| Confirm no status check | CPLPCLT | Business Logic | MEDIUM |
| Change CP-STATUS='8' via CEBR/File-AID | PCIF VSAM | Operations | PREREQUISITE |
| No change needed | CPS948, MBI programs, CPCPTB | — | — |

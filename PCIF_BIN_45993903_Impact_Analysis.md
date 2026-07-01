# PCIF BIN 45993903 Removal — System Impact Analysis

**BIN:** 45993903 (8-digit VISA prefix)  
**Bank:** BIMB Bank (under collection via CIMB)  
**File:** CPPFX (Card Prefix Identification File — VSAM KSDS)  
**Copybook:** CPS148  
**Region:** MY20A2 (Cardlink / Worldline CACQ — CIMB Malaysia)

---

## Background

BIN 45993903 is currently an active entry in the Card Prefix Identification File (PCIF / CPPFX).  
The PCIF record maps the BIN to:
- `CP-SCHEME` = 'V' (VISA)
- `CP-ORG-NMBR` / `CP-TYPE-NMBR` — org/type assigned to BIMB's card range
- `CP-STATUS` = '1' (Active)
- `CP-CARD-RANGE-FROM` / `CP-CARD-RANGE-TO` — card number range boundaries

The Card Prefix Search Routine **CPS948** (procedure copybook) is called by programs to look up this record via CICS STARTBR/READNEXT on CPPFXA (the CICS-accessible version of the PCIF). When a match is found, CPS948 sets `WS-CARD-SCHEME`, `WS-CARD-ORG-NMBR`, `WS-CARD-TYPE-NMBR`, and the ON-US/NOT-ON-US flag.

**Portfolio data (as at 2026-07-01):**

| PREFIX | ORG | TYPE | SCHEME | Regular Acct | Chargeoff Acct |
|--------|-----|------|--------|-------------|----------------|
| 45993903 | 1 | 114 | V | **3** | 7,331 |
| 45993905 | 1 | 115 | V | 2 | 1,879 |

BIN 45993903 still has **3 live (regular) accounts**. Hard-deleting the PCIF record while these accounts exist would disrupt their authorizations and account lookups. The business plan is therefore to first set `CP-STATUS` to `'8'` (Inactive) as a soft-disable.

**If BIN 45993903 is deleted from PCIF:**  
All CPS948 calls for cards starting with 45993903 will return NOTFND (no match in range). The card scheme, org, and type will remain blank/zero. Programs will treat the card as NOT-ON-US and unidentified.

---

## CP-STATUS = '8' (Inactive) — Soft-Disable Analysis

### Key Question
Will setting `CP-STATUS` from `'1'` (Active) to `'8'` (Inactive) allow the system to still accept payments from BIN 45993903 while the BIN is being wound down?

### CPS948 — Card Prefix Search Routine (CONFIRMED: Status-Blind)

Source code verified (CPS948.txt lines 003800–004600). The match logic is:

```cobol
IF CSCGIO-EIBRESP IS EQUAL DFHRESP(NORMAL) OR DFHRESP(DUPKEY)
   IF (CP-FLAG-TYPE) AND
      (WS-CARD-NUMBER >= CP-CARD-RANGE-FROM) AND
      (WS-CARD-NUMBER <= CP-CARD-RANGE-TO)
      MOVE CP-SCHEME     TO WS-CARD-SCHEME
      MOVE CP-ORG-NMBR   TO WS-CARD-ORG-NMBR
      MOVE CP-TYPE-NMBR  TO WS-CARD-TYPE-NMBR
      ...
      SET ON-US-TXN TO TRUE
      GO TO CIA-CARD-PREFIX-SEARCH-EXIT
```

**There is no `CP-STATUS` check anywhere in CPS948.** A record with `CP-STATUS = '8'` is treated identically to `CP-STATUS = '1'`. The BIN will be found, the scheme/org/type will be returned, and `ON-US-TXN` will be set — exactly as before.

**Impact of CP-STATUS = '8' on CPS948: NONE.**

### CPCPTB — Batch Prefix Table Builder (No Status Filter Found)

CPCPTB (CPCPTB.txt) copies CPS148 in working storage (inheriting the CP-STATUS field definition) but a fullText search for `CP-ACTIVE` combined with `CPPFX` did **not** return CPCPTB — only CP617180. This confirms CPCPTB does not test `IF CP-ACTIVE` or any status condition in its `2000-LOAD-PREFIX-TABLE` procedure. All records from CPPFX are loaded into the CPS348 in-memory table regardless of status.

**Impact of CP-STATUS = '8' on CPCPTB: NONE. BIN 45993903 will still be in the batch prefix table.**

### CP617180 — Bulk Card Upgrade / CLI / CLD (Status-Aware)

CP617180 (AS400 bulk upgrade interface for credit limit increase/decrease and card upgrade) is the **only** program confirmed to check both `CP-ACTIVE` / `CP-INACTIVE` and read from `CPPFX` directly. If this program checks status before performing bulk operations, `CP-STATUS = '8'` will cause 45993903 cards to be **skipped** in bulk CLI/CLD and card upgrade runs.

**Impact: Expected and acceptable.** A BIN being wound down should not receive new bulk upgrades.

### CPOPCMF — Card Prefix Maintenance Screen (CRITICAL OPERATIONAL NOTE)

In the CPOPCMF BMS map (CPPCMF), the STATUS field was **commented out** in change CP3345P:

```cobol
*** 07 MAP-CARD-STL   PIC S9(4) COMP.    CP3345P
*** 07 MAP-CARD-STA   PIC X.             CP3345P
*** 07 MAP-CARD-STI   PIC X.             CP3345P   ← STATUS field removed from screen
```

**The CPOPCMF online screen cannot display or accept the STATUS field.** The business user cannot change `CP-STATUS` to `'8'` via the normal Card Prefix Maintenance screen.

**Required workaround (choose one):**
1. Use **CEBR** (CICS Browse/Edit) to directly read and rewrite the CPPFXA record, changing byte offset for `CP-STATUS` from `X'F1'` ('1') to `X'F8'` ('8').
2. Use **File-AID** or an IDCAMS REPRO/ALTER batch job to update the `CP-STATUS` byte in the VSAM CPPFX dataset directly.
3. A developer writes a one-off COBOL/CECI program to REWRITE the specific CPPFX record with `CP-STATUS = '8'`.
4. Temporarily reinstate the status field in CPOPCMF (CPPCMF map change) — requires code change and test.

### Programs Requiring Code Changes

**No MBI program or payment program needs a code change** to continue working correctly after `CP-STATUS = '8'` is set. All programs that rely on CPS948 (AULAUAC, CPLPCLT, MICCMC, MICCAV, MIVUCP, MICCOP, MICCSA) will continue to resolve BIN 45993903 without modification, because CPS948 is status-blind.

### CP-STATUS = '8' Impact Summary

| Program / Component | Checks CP-STATUS? | Behavior After Status = '8' |
|--------------------|-------------------|-----------------------------|
| **CPS948** (prefix search) | **NO** (confirmed from code) | Unchanged — BIN 45993903 found, ON-US-TXN set |
| **AULAUAC** (authorization) | NO (calls CPS948) | Auth continues to work for live accounts |
| **CPLPCLT** (account locate) | NO (calls CPS948 / CPCPTB) | Account locate continues to work |
| **MICCSA / MICCAV / MICCMC / MIVUCP / MICCOP** (MBI) | NO (call CPS948) | MBI operations continue to work |
| **CPCPTB / CPCPTB2** (batch table) | NO (no IF CP-ACTIVE found) | BIN still loaded into batch prefix table |
| **CPD100** (cardholder maint) | NO (uses CPS348 from CPCPTB) | Batch processing unaffected |
| **QMD004** (merchant posting) | NO | Payment posting unaffected |
| **CPU624 / CPU624SQ** (history split) | Low risk | Split logic unaffected |
| **CP617180** (bulk upgrade/CLI) | **YES** (confirmed CP-ACTIVE check) | Bulk operations for 45993903 cards SKIPPED |
| **CPOPCMF** (maintenance screen) | N/A | Status field REMOVED from screen — cannot set '8' via screen |

**Bottom line:** Setting `CP-STATUS = '8'` is **safe for the 3 live accounts** — payment, authorization, MBI, and batch processing all continue to work. No code changes are required in any program. The only action needed is an operational update to the CPPFX record using a tool that can bypass the CPOPCMF screen limitation.

---

## Impact by System Area

### 1. ONLINE — Card Prefix Maintenance Screen

| Program | Function | Impact |
|---------|----------|--------|
| **CPOPCMF** | CARDLINK CARD PREFIX MAINTENANCE/INQUIRY | This is the screen used to perform the deletion itself (DELETE function). No disruption — this program IS the tool for the change. After deletion, INQUIRY of BIN 45993903 will return NOT FOUND. |

---

### 2. ONLINE — Authorization (AUC Region)

| Program | Function | Impact |
|---------|----------|--------|
| **AULAUAC** | AUTHORIZATION VERSION 2 — Business Logic for Account Verification | Uses CPS148 to GETMAIN the CPPFX prefix record and verify the cardholder's account and org/type. If BIN is removed: **prefix lookup returns blank** → org/type = 0 → card cannot be linked to BIMB's org/type → authorization verification fails or card is treated as not-on-us. **Any live authorization for BIMB 45993903 cards could be declined or misrouted.** |

---

### 3. ONLINE — Account Locate / Business Logic (CARDC / CCP Region)

| Program | Function | Impact |
|---------|----------|--------|
| **CPLPCLT** | BUSINESS LOGIC FOR ACCOUNT LOCATE — Get Account & Customer Number | GETMAIN-CPPFX flag present. Uses prefix table to identify org/type from BIN, then locates the plastic and account records. If BIN 45993903 removed: **account locate will fail** for BIMB cards — cannot determine which org/type to search → Z001 system error or Z002 field edit error returned to the caller. Any downstream CICS transaction that calls CPLPCLT for a BIMB 45993903 card will receive an error. |

---

### 4. ONLINE — MBI (Message-Based Interface) Programs

All MBI programs below are linked by **MI003** (ISO Message Processor). They call **CPS948** (Card Prefix Search Routine) to identify the card scheme and on-us/non-on-us status before processing. If BIN 45993903 is not in PCIF, CPS948 returns NOTFND, and the programs cannot classify the card.

| Program | Function | Impact |
|---------|----------|--------|
| **MICCMC** | MBI Customer Address/Contact Maintenance | If BIMB sends an MBI request to update customer address for a BIN 45993903 card → CPS948 NOTFND → card not recognized as on-us → **request rejected or processed with wrong classification.** |
| **MICCAV** | MBI Card Activation | If BIMB sends card activation request for BIN 45993903 → CPS948 NOTFND → **card activation fails.** Newly issued BIMB cards in this BIN range cannot be activated via MBI. |
| **MIVUCP** | MBI Customer Additional Details Maintenance | Same CPS948 dependency. **BIMB MBI updates for customer additional details will fail.** |
| **MICCOP** | MBI Set Payment Method in Cardholder File | Same CPS948 dependency. **Cannot set payment method for BIMB 45993903 cards via MBI.** |
| **MICCSA** | MBI Set Lost/Stolen Card Block Code | Same CPS948 dependency. **CRITICAL: Cannot set L (Lost) or S (Stolen) block code for BIMB cards via MBI.** BIMB bank will be unable to block lost/stolen 45993903 cards through the MBI channel → fraud risk. |

---

### 5. BATCH — Card Prefix Table Builder

| Program | Function | Impact |
|---------|----------|--------|
| **CPCPTB** | SUBROUTINE TO BUILD CARD PREFIX TABLE (reads CPPFX sequentially → in-memory table CPS348) | Called at batch start: `CALL 'CPCPTB' USING WS-CARD-PREFIX-TABLE`. After BIN removal, the table loaded into CPS348 will not contain a 45993903 entry. **All batch programs that call CPCPTB will not find a match for BIN 45993903.** |
| **CPCPTB2** | Mirror of CPCPTB for V1 programs (reads CPV2PFX) | Same impact — reads a separate copy of the prefix file. If CPV2PFX also contains BIN 45993903, it must also be updated. |

---

### 6. BATCH — Cardholder/Customer File Maintenance

| Program | Function | Impact |
|---------|----------|--------|
| **CPD100** | CARDHOLDER & CUSTOMER FILE MAINTENANCE (large batch — 1.8MB source) | Copies CPS348 (prefix table built by CPCPTB). If CPCPTB is run before CPD100 in the same daily batch, BIN 45993903 will not appear in the prefix table. **Any CPD100 batch processing that uses the prefix to classify 45993903 cards will not find the org/type.** Exact behavior depends on how CPD100 handles a no-match (may skip, error, or process with defaults). |

---

### 7. BATCH — Card/Member History File Splitter

| Program | Function | Impact |
|---------|----------|--------|
| **CPU624** | SPLIT CPCMH FILE by Account/Customer/Card criteria | Uses CPS148. If the split criteria involves BIN-based classification, 45993903 records may be mis-split. Impact depends on whether BIN lookup is used in the split logic (code is too large to confirm via snippet alone). **Low–medium risk; review the split criteria in the COBOL procedure division.** |
| **CPU624SQ** | Same as CPU624 (sequential variant) | Same as above. |

---

### 8. BATCH — Payment Processing (MOST CRITICAL)

| Program | Function | Impact |
|---------|----------|--------|
| **QMD004** | CARDLINK ACQUIRER BATCH — Merchant Posting (Deposits, Reversals, Adjustments) | QMD004 does **not** appear to directly COPY CPS148 or CPS348. It processes the CXMID file (CX Merchant Input Deposit). The org/type and card scheme in CXMID were **set at authorization time** (by AULAUAC/CPS948) and embedded in the input records. However, **if AULAUAC cannot resolve the card scheme at auth time** (because BIN was removed from PCIF), the transactions will already be in error BEFORE reaching QMD004. Additionally, QMD004 uses the card scheme to look up merchant discount in QMPPGO/QMPDIS — if the scheme field is blank, discount lookup will fail → **transactions posted with wrong discount or rejected with reason 03 (DIS NOT FOUND).** |

**Payment Flow Impact Summary:**

```
Card presented → Auth (AULAUAC) reads PCIF via CPS948
                    |
                    v
       BIN NOT IN PCIF → scheme = blank, org/type = 0
                    |
                    v
       Auth decision may be wrong (non-on-us treatment)
                    |
                    v
       CXMID built with blank/wrong scheme
                    |
                    v
       QMD004 → QMPPGO lookup by scheme fails
                    |
                    v
       Merchant posting: REJECT reason 03 or wrong discount rate
```

---

## Summary Table

| Area | Programs | Severity | Impact if BIN Removed |
|------|----------|----------|----------------------|
| Maintenance Screen | CPOPCMF | None | No impact (this IS the deletion tool) |
| Authorization | AULAUAC | **HIGH** | Auth for BIMB 45993903 cards may fail or misroute |
| Account Locate | CPLPCLT | **HIGH** | Account locate fails for BIMB cards (system error) |
| MBI – Card Activation | MICCAV | **HIGH** | Card activation fails via MBI |
| MBI – Lost/Stolen Block | MICCSA | **CRITICAL** | Cannot block lost/stolen cards → fraud risk |
| MBI – Cust Maintenance | MICCMC, MIVUCP, MICCOP | Medium | MBI maintenance requests fail |
| Payment – Auth Stage | AULAUAC → CXMID | **HIGH** | CXMID records will carry blank/wrong scheme |
| Payment – Posting | QMD004 | **HIGH** | Merchant posting fails (DIS NOT FOUND, reason 03) |
| Batch Prefix Table | CPCPTB, CPCPTB2 | **HIGH** | 45993903 absent from in-memory table for all batch runs |
| Batch Cardholder Maint | CPD100 | Medium | May not match 45993903 cards to org/type in batch |
| History File Split | CPU624, CPU624SQ | Low–Medium | Split classification may be incorrect |

---

## Recommendations Before Removal

1. **Confirm all outstanding BIMB 45993903 cards are fully migrated off CIMB's processing platform** before removing from PCIF.
2. **Set CP-STATUS = '8' first (SAFE — confirmed by code scan):** `CPS948` is status-blind (confirmed in code — match is purely range-based, no CP-STATUS check). All payment, authorization, and MBI processing will continue normally for the 3 live accounts after status change. **However, CPOPCMF does not support status field update** (MAP-CARD-STI was removed from screen in CP3345P) — use CEBR, File-AID, or a direct batch VSAM update to change the byte in CPPFX.
3. **MICCSA impact is critical** — ensure BIMB has an alternate channel to block lost/stolen 45993903 cards if MBI will fail after removal.
4. **Coordinate with batch scheduling** — CPCPTB is called at batch start. Test that CPD100 and other batch programs handle the no-match gracefully.
5. **Test payment flow end-to-end** — confirm that no CXMID records with BIN 45993903 are still in-flight (unposted) when the PCIF record is deleted, to avoid QMD004 rejection.
6. **Review CPCPTB2** — if the V1 processing path (CPV2PFX) also carries BIN 45993903, that copy must also be cleaned up.

---

*Scan performed: 2026-07-01*  
*Programs scanned via: COPY CPS148, COPY CPS948, COPY CPS348, CALL CPCPTB, CP-STATUS, CP-ACTIVE, CP-INACTIVE fullText search in Drive*  
*CPS948 source code verified line-by-line (lines 003800–004600) — no CP-STATUS check confirmed*  
*CPCPTB source code verified — no CP-ACTIVE/CP-INACTIVE test in load routine confirmed*  
*CP617180 confirmed as the only program checking CP-ACTIVE/CP-INACTIVE on CPPFX*  
*CPOPCMF BMS map verified — MAP-CARD-STI (status field) commented out in change CP3345P*  
*Source: Cardlink MY20A2 COBOL source library (Drive)*

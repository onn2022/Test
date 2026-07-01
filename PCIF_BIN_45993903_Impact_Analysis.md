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

**If BIN 45993903 is deleted from PCIF:**  
All CPS948 calls for cards starting with 45993903 will return NOTFND (no match in range). The card scheme, org, and type will remain blank/zero. Programs will treat the card as NOT-ON-US and unidentified.

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
2. **Check the STATUS field** first: change `CP-STATUS` from '1' (Active) to '8' (Inactive) on the PCIF record via CPOPCMF as a first step. Inactive status may be respected by CPS948 (verify in code), allowing a soft-disable before hard delete.
3. **MICCSA impact is critical** — ensure BIMB has an alternate channel to block lost/stolen 45993903 cards if MBI will fail after removal.
4. **Coordinate with batch scheduling** — CPCPTB is called at batch start. Test that CPD100 and other batch programs handle the no-match gracefully.
5. **Test payment flow end-to-end** — confirm that no CXMID records with BIN 45993903 are still in-flight (unposted) when the PCIF record is deleted, to avoid QMD004 rejection.
6. **Review CPCPTB2** — if the V1 processing path (CPV2PFX) also carries BIN 45993903, that copy must also be cleaned up.

---

*Scan performed: 2026-07-01*  
*Programs scanned via: COPY CPS148, COPY CPS948, COPY CPS348, CALL CPCPTB fullText search in Drive*  
*Source: Cardlink MY20A2 COBOL source library (Drive)*

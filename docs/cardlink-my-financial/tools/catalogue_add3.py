# -*- coding: utf-8 -*-
"""Fourth tranche — Corporate Card Module (CCOM), the monthly interest method, and scheme gaps."""

CATALOGUE_4 = [
# ---------------- Monthly interest method (CPOPCPO) ----------------
("MINT-01","Interest — monthly method","Monthly rate from the annual rate",
 "The alternative interest method works monthly rather than daily: the annual rate (plus adjustment) is divided by twelve.",
 "COMPUTE WS-RATE1 = (CM-CI-RATE-1 + CM-CI-ADJ-1) / 12\nCOMPUTE WS-RATE2 = (CM-CI-RATE-2 + CM-CI-ADJ-2) / 12\nCOMPUTE WS-RATE3 = (CM-CI-RATE-3 + CM-CI-ADJ-3) / 12",
 "CPOPCPO","8100-COMPUTE-MONTHLY-STD-INTR",1259,"CM-CI-RATE-1/2/3, CM-CI-ADJ-1/2/3",
 "A flat /12, not a compounded monthly equivalent. This is a genuinely separate method from the daily "
 "accrual documented in INT-01..INT-08, not a restatement of it."),

("MINT-02","Interest — monthly method","Average daily balance",
 "The accumulated balance-times-days figure is divided by the accumulated day count to give the average daily balance.",
 "MOVE CM-AGGR-CASH-BALANCE TO WS-AMOUNT\nADD CM-AGGR-CASH2-BALANCE TO WS-AMOUNT\nCOMPUTE WS-AMOUNT = WS-AMOUNT / CM-AGGR-CASH-DAYS",
 "CPOPCPO","8100-COMPUTE-MONTHLY-STD-INTR",1273,"CM-AGGR-CASH-BALANCE, CM-AGGR-CASH-DAYS",
 "This is what INT-15's accumulator is for. Guarded by CM-AGGR-CASH-DAYS > ZERO."),

("MINT-03","Interest — monthly method","Balance used to choose the rate band",
 "Where the product combines retail and cash for banding, the band is selected on the combined balance across "
 "all five sub-buckets — even though the charge is then applied to this bucket's average balance alone.",
 "IF TCIV-COMB-RTLCSH-1RATE (2)\n  COMPUTE WSI-COMB-BAL ROUNDED =\n    CM-AGGR-CASH-BALANCE + CM-AGGR-RTL-BALANCE\n    + CM-AGGR-CASH2-BALANCE + CM-AGGR-RTL2-BALANCE\n    + CM-AGGR-RTL3-BALANCE\nELSE\n  MOVE WS-AMOUNT TO WSI-COMB-BAL",
 "CPOPCPO","8100-COMPUTE-MONTHLY-STD-INTR",1275,"TCIV-COMB-RTLCSH-1RATE, WSI-COMB-BAL",
 "Tier chosen on the combined balance, charged on the bucket balance. A high retail balance can therefore "
 "push cash interest into a higher band."),

("MINT-04","Interest — monthly method","Single-band monthly interest",
 "With no band limit, or a combined balance under the first limit, the whole average balance is charged at rate 1.",
 "IF CM-CI-LIMIT-1 = ZERO OR WSI-COMB-BAL < CM-CI-LIMIT-1\n  COMPUTE CM-CASH-ACCRUED-INTR ROUNDED = WS-AMOUNT * WS-RATE1",
 "CPOPCPO","8100-COMPUTE-MONTHLY-STD-INTR",1286,"CM-CI-LIMIT-1",""),

("MINT-05","Interest — monthly method","Two-band monthly interest",
 "Above the first limit the charge splits: limit 1 at rate 1, the remainder of the average balance at rate 2.",
 "COMPUTE CM-CASH-ACCRUED-INTR ROUNDED =\n  (CM-CI-LIMIT-1 * WS-RATE1)\n  + ((WS-AMOUNT - CM-CI-LIMIT-1) * WS-RATE2)",
 "CPOPCPO","8100-COMPUTE-MONTHLY-STD-INTR",1290,"CM-CI-LIMIT-1, TCIV-SPLIT-RTLCSH-MULTIRATE",""),

("MINT-06","Interest — monthly method","Three-band monthly interest",
 "The full monthly ladder, mirroring the daily three-tier shape.",
 "COMPUTE CM-CASH-ACCRUED-INTR ROUNDED =\n  (CM-CI-LIMIT-1 * WS-RATE1)\n  + ((CM-CI-LIMIT-2 - CM-CI-LIMIT-1) * WS-RATE2)\n  + ((WS-AMOUNT - CM-CI-LIMIT-2) * WS-RATE3)",
 "CPOPCPO","8100-COMPUTE-MONTHLY-STD-INTR",1295,"CM-CI-LIMIT-1, CM-CI-LIMIT-2",""),

("MINT-07","Interest — monthly method","Per-diem for display",
 "The two accrued-interest buckets added together give the per-diem figure shown online.",
 "COMPUTE WS-PER-DIEM = CM-CASH-ACCRUED-INTR + CM-RTL-ACCRUED-INTR",
 "CPOPCPO","(online enquiry)",1013,"CM-CASH-ACCRUED-INTR, CM-RTL-ACCRUED-INTR",""),

("MINT-08","Interest — monthly method","Balance net of over-limit payments",
 "Over-limit payments already received are removed from the displayed balance.",
 "COMPUTE CUR-AMT = CM-CURR-BALANCE - (CM-OL-CASH-PYMT + CM-OL-RTL-PYMT)",
 "CPOPCPO","(online enquiry)",1044,"CM-OL-CASH-PYMT, CM-OL-RTL-PYMT",""),

# ---------------- Corporate card limits (CCOM) ----------------
("CCOM-01","Corporate card limits (CCOM)","Available cap limit",
 "The corporate cap limit, grossed up by its variance multiplier, less everything already committed "
 "(accumulated authorisations plus current balance). Never negative.",
 "COMPUTE WS300-KC-AVL-CAP-LMT ROUNDED =\n  (LMTC-CAP-LMT * LMTC-CAP-VAR)\n  - (WS300-KC-ACCUM-AMNT + WS300-KC-ACCUM-CURR-BAL)\n  ON SIZE ERROR MOVE 999999999999999.99 TO WS300-KC-AVL-CAP-LMT\nIF WS300-KC-AVL-CAP-LMT < 0  MOVE ZEROS TO WS300-KC-AVL-CAP-LMT",
 "KCC809","KC809-CAP-AVL-NO-LAAD",236,"LMTC-CAP-LMT, LMTC-CAP-VAR",
 "The size-error sentinel 999999999999999.99 means 'treat as unlimited'. Same variance-multiplier shape "
 "as TCM-OVER-LIMIT on the consumer side (LMT-03)."),

("CCOM-02","Corporate card limits (CCOM)","Cap limit utilisation",
 "Committed amount over the cap limit, as a proportion. A size error yields zero rather than abending.",
 "COMPUTE WS300-KC-CAP-LMT-UTIL ROUNDED =\n  (WS300-KC-ACCUM-AMNT + WS300-KC-ACCUM-CURR-BAL) / LMTC-CAP-LMT\n  ON SIZE ERROR MOVE 0.00 TO WS300-KC-CAP-LMT-UTIL",
 "KCC809","KC809-CAP-AVL-CAL",248,"LMTC-CAP-LMT",
 "Note the denominator is the raw cap, not the variance-grossed cap — so utilisation can exceed 100%."),

("CCOM-03","Corporate card limits (CCOM)","Available OSL limit, cycle and domestic",
 "The outstanding-spend limit for the cycle, grossed up by the OSL variance, less what has accumulated this cycle.",
 "COMPUTE WS300-KC-AVL-CYC-LMT-D-O ROUNDED =\n  (WS300-KC-OSL-CYC-LMT-DOM * LMTC-OSL-VAR)\n  - WS300-KC-ACCUM-CYC-AMT-DOM\n  ON SIZE ERROR MOVE 999999999999999.99 ...\nIF < 0 MOVE ZEROS",
 "KCC809","KC809-CYC-DLY-NO-LAAO",443,"WS300-KC-OSL-CYC-LMT-DOM, LMTC-OSL-VAR",
 "The identical shape repeats four ways: cycle/daily x domestic/international."),

("CCOM-04","Corporate card limits (CCOM)","Available transaction count",
 "Corporate cards are limited by transaction count as well as amount; the remaining count is the limit less what is used.",
 "COMPUTE WS300-KC-AVL-CYC-CNT-DOM =\n  WS300-KC-OSL-CYC-CNT-DOM - WS300-KC-ACCUM-CYC-NBR-DOM\n  ON SIZE ERROR MOVE 9999999 ...\nIF < 0 MOVE ZEROS",
 "KCC809","KC809-CYC-DLY-NO-LAAO",454,"WS300-KC-OSL-CYC-CNT-DOM",
 "A count limit is a control the consumer side does not have. A card can be declined for too many "
 "transactions even with limit to spare."),

("CCOM-05","Corporate card limits (CCOM)","Utilisation on amount and on count",
 "Both the amount limit and the count limit carry their own utilisation percentage.",
 "COMPUTE WS300-KC-CYC-DOM-LMT-UTIL ROUNDED =\n  WS300-KC-ACCUM-CYC-AMT-DOM / WS300-KC-OSL-CYC-LMT-DOM\nCOMPUTE WS300-KC-CYC-DOM-CNT-UTIL ROUNDED =\n  WS300-KC-ACCUM-CYC-NBR-DOM / WS300-KC-OSL-CYC-CNT-DOM\n  (both ON SIZE ERROR MOVE 0.00)",
 "KCC809","KC809-CYC-DLY-NO-LAAO",464,"WS300-KC-ACCUM-CYC-*","Eight utilisation figures in all, across the four dimensions."),

("CCOM-06","Corporate card limits (CCOM)","Per-transaction control limit at authorisation",
 "The single-transaction limit is the table limit times its variance multiplier, chosen by domestic or international.",
 "COMPUTE WS-KC-TOT-CTRL-LMT = LMTC-TXN-DOM * LMTC-TXN-VAR\n(international) COMPUTE WS-KC-TOT-CTRL-LMT = LMTC-TXN-INTL * LMTC-TXN-VAR",
 "KCLAUIN","(limit sequence check)",1251,"LMTC-TXN-DOM, LMTC-TXN-INTL, LMTC-TXN-VAR",
 "KCLAUIN is the commercial-card limit authorisation sequence check — it walks the limit hierarchy in order."),

("CCOM-07","Corporate card limits (CCOM)","Daily accumulation tested at authorisation",
 "Daily exposure is retail plus cash spend for the day plus the amount now being authorised.",
 "COMPUTE WS-KC-ACCUM-AMT =\n  WS300-KC-RTL-DLY-AMT-DOM + WS300-KC-CSH-DLY-AMT-DOM\n  + WS300-KC-BASE-AMOUNT\nCOMPUTE WS-KC-TOT-CTRL-LMT = LMTC-OSL-DLY-LMT-DOM * LMTC-OSL-VAR",
 "KCLAUIN","B050-CHK-CARDMEMBER-OSL-DLY",1302,"WS300-KC-BASE-AMOUNT, LMTC-OSL-DLY-LMT-DOM",
 "WS300-KC-BASE-AMOUNT is the requested amount converted to the corporate base currency."),

("CCOM-08","Corporate card limits (CCOM)","High utilisation against the cap",
 "Peak utilisation for the reporting period: total new balances over the cap limit.",
 "COMPUTE WS-R13-HI-UTIL-PER-CAP ROUNDED =\n  ((WS-R13-NEW-BAL (1) + WS-R13-NEW-BAL (2))\n   + (KCICSH-NEW-BAL (1) + KCICSH-NEW-BAL (2))) / KCLMTR-CAP-LMT",
 "KCD140","(spending history update 2)",1018,"KCLMTR-CAP-LMT",
 "Parallel figures exist for OSL domestic and OSL international utilisation."),

("CCOM-09","Corporate card limits (CCOM)","Total cycle OSL limit",
 "Domestic and international cycle limits added for the combined figure shown on reports.",
 "COMPUTE WS201-TOT-OSL-CYC-LMT-TOT =\n  KCLMTCH-OSL-CYC-LMT-DOM + KCLMTCH-OSL-CYC-LMT-INTL",
 "KCD310","D250-FORMAT-PLASTIC-BASIC-INFO",587,"KCLMTCH-OSL-CYC-LMT-*",""),

# ---------------- Corporate card multi-currency ----------------
("CCCY-01","Corporate card limits (CCOM)","Convert balances to the corporate base currency",
 "Every amount on a corporate plastic is multiplied by the exchange rate to express it in the corporate "
 "account's base currency before limits are tested or totals struck.",
 "COMPUTE WS-TMP-NEW-BAL (idx) = WS-CCY-NEW-BAL (idx) * WS-CCY-XCHG-RTE\nCOMPUTE WS-TMP-HI-BALANCE = WS-CCY-HI-BALANCE * WS-CCY-XCHG-RTE\nCOMPUTE WS-TMP-TXN-FEE (idx) = WS-CCY-TXN-FEE (idx) * WS-CCY-XCHG-RTE",
 "KCD136","C600-TOTAL-000",704,"WS-CCY-XCHG-RTE",
 "Corporate cards in a group can be denominated in different currencies; the group limit is enforced in one "
 "base currency, so everything is converted first."),

("CCCY-02","Corporate card limits (CCOM)","Convert outstanding authorisations and last payment",
 "The same conversion applied to outstanding authorisations, last payment and high balance.",
 "COMPUTE KCSHASH-AMT-OUTST-AUTH = KCSHASH-AMT-OUTST-AUTH * WS-CCY-XCHG-RTE\nCOMPUTE WS-CNV-LST-PYMT-AMT = KCSHASH-LST-PYMT-AMT * WS-CCY-XCHG-RTE\nCOMPUTE WS-CNV-HI-BALANCE = KCSHASH-HI-BALANCE * WS-CCY-XCHG-RTE",
 "KCD122","D600-CONV-AMT-FIELDS",1127,"WS-CCY-XCHG-RTE",
 "Note the in-place form: KCSHASH-AMT-OUTST-AUTH overwrites itself, so the record is converted once only."),

("CCOM-10","Corporate card limits (CCOM)","Corporate current and disputed balance",
 "Corporate balances are held as a two-element array (retail and cash) and summed for the account figure.",
 "COMPUTE WS-CURR-BAL = KCSHASH-NEW-BAL (1) + KCSHASH-NEW-BAL (2)\nCOMPUTE WS-DISP-BAL = KCSHASH-DISPUTED-BAL (1) + KCSHASH-DISPUTED-BAL (2)\nCOMPUTE WS-PAYMENT = KCSHASH-OL-CASH-PYMT + KCSHASH-OL-RTL-PYMT",
 "KCD122","C300-POP-LAAD",515,"KCSHASH-NEW-BAL, KCSHASH-DISPUTED-BAL",""),

("CCOM-11","Corporate card limits (CCOM)","Corporate statement figures",
 "Opening balance, statement balance, new charges, credits and cash advance are each struck from the "
 "two-by-two retail/cash by domestic/international bucket matrix.",
 "COMPUTE WS201-OPEN-BAL = KCSHASH-NEW-BAL (1) + KCSHASH-NEW-BAL (2)\nCOMPUTE WS201-NEW-CHRGS = KCSHASH-RC-AMT-DB (1 1) + KCSHASH-RC-AMT-DB (2 1)\n  + KCSHASH-RC-AMT-DB (1 2) + KCSHASH-RC-AMT-DB (2 2) + ...\nCOMPUTE WS201-CSH-ADV = KCSHASH-RC-AMT-DB (2 1) - KCSHASH-RC-AMT-CR (2 1)\n  + KCSHASH-RC-AMT-DB (2 2) - KCSHASH-RC-AMT-CR (2 2)",
 "KCD310","D400-FIELDS-ACCUM",640,"KCSHASH-RC-AMT-DB, KCSHASH-RC-AMT-CR",
 "First subscript is retail(1)/cash(2), second is domestic(1)/international(2) — hence cash advance takes "
 "only the (2,x) cells."),

("CCOM-12","Corporate card limits (CCOM)","Corporate fee hash totals",
 "Cash advance, over-limit and membership fees are hash-totalled with their reversals held separately, "
 "so a reversal never silently cancels the original in the control total.",
 "COMPUTE WS-HASH-CA-PER-FEE = WS-HASH-CA-PER-FEE + KCHASHI-CA-PER-FEE\nCOMPUTE WS-HASH-CA-PER-FEE-REV = WS-HASH-CA-PER-FEE-REV + KCHASHI-CA-PER-FEE-REV\nCOMPUTE WS-HASH-OVRLMT-FEE = ... / -REV\nCOMPUTE WS-HASH-MBR-FEE = ... / -REV",
 "KCD120","C200-POP-REC",475,"KCHASHI-* fee fields",
 "Keeping the reversal in its own bucket is what lets the control report prove both sides."),

# ---------------- Scheme clearing gaps ----------------
("FX-07","Currency conversion","Scheme amounts divided by the currency exponent",
 "Transaction, billing, reimbursement-fee, cashback and surcharge amounts are each divided by ten to the "
 "power of their own currency exponent — the exponent differs per field.",
 "COMPUTE WS-AMT = CXS120-TXN-AMT / (10 ** CXS120-TXN-CCY-EXP)\nCOMPUTE WS-AMT = CXS120-BILLING-AMT / (10 ** CXS120-BILLING-CCY-EXP)\nCOMPUTE WS-AMT = CXS120-NATIONAL-REIMB-FEE / (10 ** WS-CCY-EXP)\nCOMPUTE WS-AMT = CXS120-CASHBACK / (10 ** WS-CCY-EXP)",
 "CXCV030","(Visa outgoing build)",1932,"CXS120-TXN-CCY-EXP, CXS120-BILLING-CCY-EXP",
 "Transaction and billing currency can differ, so each carries its own exponent."),

("FX-08","Currency conversion","Surcharge to major units",
 "The surcharge is held as a numeric string and rescaled by the transaction currency exponent.",
 "COMPUTE WS-SUR-AMT = WS-SUR-AMT-NUM-R / (10 ** CXS120-TXN-CCY-EXP)",
 "CXCV030","(Visa outgoing build)",2512,"CXS120-TXN-CCY-EXP",""),

("SET-03","Merchant volume & settlement","Accepted versus rejected capture totals",
 "For a capture file, accepted value is the sales total less the credits total; rejected value adds the "
 "other-reject bucket on top.",
 "COMPUTE WS-TOTAL-AMT-ACP = WS-TC40-AMT - WS-TC41-AMT\nCOMPUTE WS-TOTAL-AMT-REJ =\n  WS-TC40-AMT-REJ - WS-TC41-AMT-REJ + WS-OTH-AMT-REJ",
 "CXCB010","(TC33 capture processing)",1474,"WS-TC40-AMT, WS-TC41-AMT",
 "TC40 is the sale record, TC41 the credit. CyberSource transactions in the TC33 capture file."),

("SET-04","Merchant volume & settlement","Credit totals negated for presentation",
 "Credit amounts are flipped in sign before the audit report is written.",
 "COMPUTE WS-TC41-AMT = WS-TC41-AMT * -1\nCOMPUTE WS-TC41-AMT-REJ = WS-TC41-AMT-REJ * -1",
 "CXCB010","(TC33 capture processing)",1591,"WS-TC41-AMT",""),

("STA-07","Merchant volume & statistics","Authorisation outcome totals",
 "Approved, declined, pickup, fraud and referral amounts are summed into the authorisation statistics total.",
 "COMPUTE CGCA-TOTAL-AMT (1) = CGCA-APPR-AMT (1) + CGCA-DECLINE-AMT (1)\n  + CGCA-PICKUP-AMT (1) + CGCA-FRAUD-AMT (1) + CGCA-REFER-AMT (1)",
 "AULAUSD","E300-FORMAT-AMT-SCR-1",1743,"CGCA-*-AMT",
 "Authorisation statistics display, accumulated by card scheme."),

("AUT-04","Credit limit & availability","Instalment reserve at issuer sub-system level",
 "The same instalment reserve adjustment as AUT-01/AUT-02, applied in the issuer sub-system at card, "
 "customer and corporate level.",
 "COMPUTE CM-AVAIL-CREDIT ROUNDED = CM-AVAIL-CREDIT\n  - (AUIS-INQ-AMOUNT-SAVE-AREA * TC-INSTL-EM-AVL-PER)\n(and the matching + form on release; CR- and CORP-CR- variants alongside)",
 "AULAISM","(issuer sub-system)",5368,"AUIS-INQ-AMOUNT-SAVE-AREA, TC-INSTL-EM-AVL-PER",
 "Four programs now carry this identical arithmetic: AUS301V, AUS301J, AUS301M and AULAISM."),
]

PROGRAMS_4 = [
 ("AULAISM","Online","Authorisation v2 — issuer sub-system business logic; available credit at card, customer and corporate level."),
 ("AULAUSD","Online","Authorisation v2 — authorisation statistics display, accumulated by card scheme."),
 ("CPOPCPO","Online","Cardholder online enquiry — carries the monthly standard interest method (average daily balance x monthly rate)."),
 ("CXCB010","Batch","CyberSource transactions in the TC33 capture file — accepted and rejected totals."),
 ("CXCV030","Batch","Visa outgoing file build — per-field currency exponent scaling."),
 ("CXU008","Batch","IPM PDS record encoding; no financial arithmetic beyond a record-length calculation."),
 ("KCC809","Copybook (online)","CCOM available limit calculation routine — cap and OSL limits, amounts and counts, with utilisation."),
 ("KCD120","Batch","CCOM cardholder account spending history update; fee hash control totals."),
 ("KCD122","Batch","CCOM plastic card cycle-to-date spending in base currency, and authorisation file update."),
 ("KCD130","Batch","CCOM band-1 spending history accumulation, program 2."),
 ("KCD136","Batch","CCOM accumulate totals for all up-link corporate accounts; base-currency conversion."),
 ("KCD140","Batch","CCOM spending history update 2 — peak utilisation against cap and OSL limits."),
 ("KCD310","Batch","CCOM preparation for account-related reports — corporate statement figures."),
 ("KCLAUIN","Online","CCOM commercial card limit authorisation sequence check."),
]

PARAMETERS_4 = [
 ("LMTC-CAP-LMT","CCOM limit control table","Corporate cap limit","Amount","CCOM-01, CCOM-02","KCC809"),
 ("LMTC-CAP-VAR","CCOM limit control table","Variance multiplier grossing up the cap limit","Multiplier","CCOM-01","KCC809"),
 ("LMTC-OSL-VAR","CCOM limit control table","Variance multiplier on outstanding-spend limits","Multiplier","CCOM-03, CCOM-07","KCC809"),
 ("WS300-KC-OSL-CYC-LMT-DOM / -INTL","CCOM limit record","Cycle outstanding-spend limit, domestic and international","Amount","CCOM-03","KCC809"),
 ("WS300-KC-OSL-CYC-CNT-DOM / -INTL","CCOM limit record","Cycle transaction count limit","Count","CCOM-04","KCC809"),
 ("LMTC-OSL-DLY-LMT-DOM / -INTL","CCOM limit control table","Daily outstanding-spend limit","Amount","CCOM-07","KCLAUIN"),
 ("LMTC-TXN-DOM / LMTC-TXN-INTL","CCOM limit control table","Single-transaction limit","Amount","CCOM-06","KCLAUIN"),
 ("LMTC-TXN-VAR","CCOM limit control table","Variance multiplier on the single-transaction limit","Multiplier","CCOM-06","KCLAUIN"),
 ("KCLMTR-CAP-LMT","CCOM limit record","Cap limit used as the utilisation denominator","Amount","CCOM-08","KCD140"),
 ("WS-CCY-XCHG-RTE","CCOM currency table","Rate converting a plastic's currency to the corporate base currency","Rate","CCCY-01, CCCY-02","KCD136"),
 ("TCIV-COMB-RTLCSH-1RATE","Product control","Whether retail and cash are combined when choosing the rate band","Flag","MINT-03","CPOPCPO"),
 ("TCIV-SPLIT-RTLCSH-MULTIRATE","Product control","Whether the multi-rate ladder applies","Flag","MINT-05","CPOPCPO"),
 ("CM-CI-LIMIT-1 / CM-CI-LIMIT-2","Cardholder master","Band boundaries for the monthly interest method","Amount","MINT-04, MINT-05, MINT-06","CPOPCPO"),
 ("CM-AGGR-CASH-DAYS","Cardholder master","Accumulated days, the divisor for average daily balance","Days","MINT-02","CPOPCPO"),
 ("CXS120-BILLING-CCY-EXP","Scheme transaction record","Billing currency exponent, separate from the transaction one","Exponent","FX-07","CXCV030"),
]

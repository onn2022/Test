# -*- coding: utf-8 -*-
"""Third tranche — computations found in the 16 further programs (CPS333 rate setting and others)."""

CATALOGUE_3 = [
# ---------------- Rate setting (CPS333) ----------------
("RATE-01","Interest — rate setting","Retail rate = product rate, plus adjustment where it applies",
 "The working retail rate for each band is the cardholder's product rate. Where the account carries a rate "
 "adjustment and it is due to be applied, the adjustment is added on top.",
 "IF NOT-APPLY-RTL1-ADJ\n  COMPUTE WSI-RATE-1 = CM-RI-RATE-1\n  COMPUTE WSI-RATE-2 = CM-RI-RATE-2\n  COMPUTE WSI-RATE-3 = CM-RI-RATE-3\nELSE\n  COMPUTE WSI-RATE-1 = CM-RI-RATE-1 + CM-RI-ADJ-1\n  COMPUTE WSI-RATE-2 = CM-RI-RATE-2 + CM-RI-ADJ-2\n  COMPUTE WSI-RATE-3 = CM-RI-RATE-3 + CM-RI-ADJ-3",
 "CPS333","CPS333-2100-SET-RI-RATE",96,"CM-RI-RATE-1/2/3, CM-RI-ADJ-1/2/3, NOT-APPLY-RTL1-ADJ",
 "This is where WSI-RATE-1/2/3 used by the interest bands (INT-03..INT-06) actually come from. "
 "CPD110 calls it as CPS333-2400-SET-CI-RATE / 2100-SET-RI-RATE rather than computing rates inline."),

("RATE-02","Interest — rate setting","Cash rate = product rate, plus adjustment where it applies",
 "The same rule on the cash side.",
 "IF NOT-APPLY-CASH1-ADJ\n  COMPUTE WSI-RATE-1 = CM-CI-RATE-1\n  COMPUTE WSI-RATE-2 = CM-CI-RATE-2\n  COMPUTE WSI-RATE-3 = CM-CI-RATE-3\nELSE\n  COMPUTE WSI-RATE-1 = CM-CI-RATE-1 + CM-CI-ADJ-1\n  COMPUTE WSI-RATE-2 = CM-CI-RATE-2 + CM-CI-ADJ-2\n  COMPUTE WSI-RATE-3 = CM-CI-RATE-3 + CM-CI-ADJ-3",
 "CPS333","CPS333-2400-SET-CI-RATE",138,"CM-CI-RATE-1/2/3, CM-CI-ADJ-1/2/3, NOT-APPLY-CASH1-ADJ",""),

("RATE-03","Interest — rate setting","Sub-bucket rates (retail 2 and 3, cash 2)",
 "Retail buckets 2 and 3 and cash bucket 2 each have their own rate set, following the same base-plus-adjustment rule.",
 "CPS333-2200-SET-RI2-RATE: COMPUTE WSI2-RATE-1 = CM-RI2-RATE-1 (+ CM-RI2-ADJ-1)\nCPS333-2300-SET-RI3-RATE: COMPUTE WSI3-RATE-1 = CM-RI3-RATE-1 (+ CM-RI3-ADJ-1)\nCPS333-2500-SET-CI2-RATE: (cash bucket 2)",
 "CPS333","CPS333-2200-SET-RI2-RATE",110,"CM-RI2-RATE-*, CM-RI3-RATE-*, CM-CI2-RATE-*",
 "Five rate sets in total, which is why an account can show five different interest figures on one statement."),

("RATE-04","Interest — rate setting","Regulatory floor and cap on every rate band",
 "Once set, every rate band is clamped between a minimum and a maximum from the min/max table — but only when "
 "that table entry is switched on. This is the ceiling-rate control.",
 "IF TC-MINMAX-EFF-FLAG (MM-IDX) NOT = 1  GO TO CPS333-5000-EXIT\nIF WSI-RATE-1 < TC-MINMAX-MIN-RATE (MM-IDX)\n  MOVE TC-MINMAX-MIN-RATE (MM-IDX) TO WSI-RATE-1\nELSE IF WSI-RATE-1 > TC-MINMAX-MAX-RATE (MM-IDX)\n  MOVE TC-MINMAX-MAX-RATE (MM-IDX) TO WSI-RATE-1\n(repeated for WSI-RATE, -2, -3 and the WSI2/WSI3 sets)",
 "CPS333","CPS333-5000-CHK-MINMAX-INT",199,"TC-MINMAX-EFF-FLAG, TC-MINMAX-MIN-RATE, TC-MINMAX-MAX-RATE",
 "The clamp is applied band by band, not to a blended rate. If the effective flag is not 1 the whole check is "
 "skipped, so an un-flagged table entry silently disables the cap."),

("INT-20","Interest — finance charge","Back-dated interest rate from the balance record",
 "When interest is recalculated for a back-dated transaction the rate comes from the account balance process "
 "record rather than the live cardholder master.",
 "COMPUTE WSI-RATE = ABP-INTR-RATE-1 + ABP-INTR-ADJ-1",
 "CPD110B","BACK-DATE-INTEREST",2197,"ABP-INTR-RATE-1, ABP-INTR-ADJ-1",
 "Using the ABP snapshot is what makes a back-dated recalculation reproduce the rate in force at the time."),

("GL-09","Provision & charge-off","Provisional interest accrual buckets",
 "Back-dated provisional interest is accumulated into its own positive and negative buckets and mirrored to the GL.",
 "COMPUTE WS-AMOUNT-GL ROUNDED = WSP-INT\nCOMPUTE WSAR-TCPI-ACCRUED ROUNDED = WSAR-TCPI-ACCRUED + WSP-INT\nCOMPUTE WSAR-TCPI-NEG-ACCRUED ROUNDED = WSAR-TCPI-NEG-ACCRUED + WSP-INT",
 "CPD110B","BDI-PROVISIONAL-INTR",2251,"WSP-INT, WSAR-TCPI-*",
 "These buckets are what CPD810's provisional roll-forward (REC-02) later proves."),

# ---------------- Merchant discount ----------------
("MDR-11","Merchant discount (MDR)","Effective MDR = global rate less base rate",
 "The effective merchant discount rate is the scheme's global rate minus the base rate, computed separately for "
 "international, domestic and on-us traffic, then applied to that channel's volume.",
 "COMPUTE WS-EMDR-M-INTL = QMTMPT-GLOBAL-RATES - WS-BSE-RTE\nCOMPUTE WS-TEMP-MDR ROUNDED =\n  WS-SUM-TMP-MC-CR-INTL * (WS-EMDR-M-INTL / 100)\nADD WS-TEMP-MDR TO WS-TOTAL-PERCENT-MC-CR-INTL",
 "CP621690","0310-PROCESS-INPUT-CARD-SCHEME",627,"QMTMPT-GLOBAL-RATES, WS-BSE-RTE",
 "Repeated per scheme (MasterCard, Visa, ...), per card type (credit, debit) and per domain "
 "(I international, D domestic, O on-us) — the same three-line shape each time."),

("MDR-12","Merchant discount (MDR)","Non-qualified sales ratio",
 "The share of outgoing sales that failed to qualify for the best interchange rate.",
 "COMPUTE WS-WORK-PERCENT ROUNDED =\n  MMD-VI-AMT-NONQUAL-SALES (2) / MMD-VI-AMT-OUTGO-SALES (2)",
 "CPM350","1210-PS-PASS-2",1194,"MMD-*-AMT-NONQUAL-SALES, MMD-*-AMT-OUTGO-SALES",
 "Non-qualified volume is priced worse, so this ratio drives merchant repricing conversations."),

("MDR-13","Merchant discount (MDR)","On-us volume as total less outgoing",
 "On-us volume (both sides of the transaction belong to the bank) is total net sales minus outgoing net sales.",
 "COMPUTE CUR-AMT ROUNDED =\n  (MMD-MC-AMT-TOTAL-SALES (X-MACT) - MMD-MC-AMT-TOTAL-RETURNS (X-MACT))\n  - (MMD-MC-AMT-OUTGO-SALES (X-MACT) - MMD-MC-AMT-OUTGO-RETURNS (X-MACT))",
 "CPOPCHM1","8220-MC-ON-US",765,"MMD-*-AMT-TOTAL-*, MMD-*-AMT-OUTGO-*",
 "On-us carries no scheme interchange, which is why it is split out before pricing."),

("MDR-14","Merchant discount (MDR)","Interchange-eligible volume",
 "Outgoing volume less the non-qualified part is what earns the standard interchange rate.",
 "COMPUTE CUR-AMT ROUNDED =\n  (MMD-MC-AMT-OUTGO-SALES (X-MACT) - MMD-MC-AMT-OUTGO-RETURNS (X-MACT))\n  - (MMD-MC-AMT-NONQUAL-SALES (X-MACT) - MMD-MC-AMT-NONQUAL-RETURNS (X-MACT))",
 "CPOPCHM1","8240-MC-IEIF",797,"MMD-*-AMT-NONQUAL-*",""),

# ---------------- Statistics ----------------
("STA-04","Merchant volume & statistics","Average ticket with a divide guard",
 "Average ticket is amount over count, but only when both are above zero, and a size error falls back to zero "
 "rather than abending.",
 "MOVE ZEROES TO WS-AVG-TKT\nIF WS-TOTAL-AMT-NET > ZERO AND WS-TOTAL-NBR-NET > ZERO\n  COMPUTE WS-AVG-TKT ROUNDED = WS-TOTAL-AMT-NET / WS-TOTAL-NBR-NET\n    ON SIZE ERROR MOVE ZEROES TO WS-AVG-TKT",
 "CPSMRPT","86200-PROCESS-REPORT-86",106,"WS-TOTAL-AMT-NET, WS-TOTAL-NBR-NET",
 "The guard-then-ON SIZE ERROR pair is the house idiom for every division in the reporting programs."),

("STA-05","Merchant volume & statistics","Projected average ticket",
 "The same average applied to projected volumes for the forward-looking columns on the merchant report.",
 "COMPUTE WS-PROJ-AVG-TKT ROUNDED =\n  WS-OT-PROJ-AMT-SALES / WS-OT-PROJ-NBR-SALES ON SIZE ERROR ...",
 "CPSMRPT","86900-REPORT-86-TOTALS",259,"WS-OT-PROJ-AMT-SALES, WS-OT-PROJ-NBR-SALES",""),

("STA-06","Merchant volume & statistics","Tier rate shown as a percentage",
 "A stored fractional rate is multiplied by 100 for display on the banded-rate report.",
 "COMPUTE WS-TIER-RATE = WS-TBL-MISC-INTR-RATE (1) * 100",
 "BNDCHNR1","(tier rate report)",771,"WS-TBL-MISC-INTR-RATE",""),

# ---------------- Currency ----------------
("FX-05","Currency conversion","Minor-unit conversion on merchant year-to-date statistics",
 "Year-to-date and prior-year scheme statistics are held in minor units and divided by 100 for reporting.",
 "COMPUTE WS-MC-YTD-OUS-SALES (X) ROUNDED = QMMSTAT-YTD-OUS-AMT (X) / 100\nCOMPUTE WS-MC-YTD-OUTGO-SALES (X) ROUNDED =\n  (QMMSTAT-YTD-DOM-AMT (X) + QMMSTAT-YTD-ITL-AMT (X)) / 100",
 "CP610850","2500-GET-SALES-RETURN",2286,"QMMSTAT-YTD-* amounts",
 "Note the direction: CP603160 multiplies by 0.01 (FX-03), this one divides by 100 — same conversion, two idioms."),

("FX-06","Currency conversion","Transaction amount to major units, with sign flip",
 "The incoming transaction amount is divided by 100 and negated where the record represents a credit.",
 "COMPUTE WS-TEMP-TXN-AMT = WS-TEMP-TXN-AMT / 100\nCOMPUTE WS-TEMP-TXN-AMT = WS-TEMP-TXN-AMT * -1",
 "CP621690","0300-PROCESS-INPUT",494,"WS-TEMP-TXN-AMT",""),

# ---------------- Authorisation ----------------
("AUT-03","Credit limit & availability","Authorisation exposure including transfers out",
 "Exposure for the limit check is the requested amount plus amounts already transferred out and outstanding authorisations.",
 "COMPUTE WS-LZD-TRF-OUT =\n  AUIS-INQ-AMOUNT-SAVE-AREA + CM-LZD-TRF-OUT + CM-AMNT-OUTST-AUTH",
 "AUS301M","(authorisation enquiry)",3005,"CM-LZD-TRF-OUT, CM-AMNT-OUTST-AUTH",
 "AUS301J and AUS301M carry the same available-credit arithmetic as AUS301V (AUT-01, AUT-02) at card, "
 "customer and corporate level."),

# ---------------- Mass maintenance ----------------
("MNT-04","Mass maintenance","Merchant-side mass maintenance",
 "The merchant file is maintained with the same percentage and absolute change factors used on the cardholder side.",
 "COMPUTE WS-PERCENT-HOLD = (WSCPS-MAINT-FIELD-NUMERIC-R (WS-MAINT) / 100) + 1\nCOMPUTE FM1-NM-09-NBR-IMP1 =\n  MMD-NBR-IMPRINTER1 + WSCPS-MAINT-FIELD-NUMERIC-R (WS-MAINT)",
 "CPU604","4210-FILL-FM-09",3270,"WSCPS-MAINT-FIELD-NUMERIC-R",
 "CPU600 maintains organisation control, CPU601 cardholder, CPU604 merchant — one pattern, three files."),

# ---------------- Settlement totals ----------------
("SET-01","Merchant volume & settlement","Scheme totals across all card brands",
 "Sales, returns, loyalty and on-us amounts are each totalled across Visa, MasterCard, JCB, debit and UnionPay.",
 "COMPUTE WS-TOTAL-SALES-AMT = WS-VS-SALES-AMT + WS-MC-SALES-AMT\n  + WS-JB-SALES-AMT + WS-DB-SALES-AMT + WS-CUP-SALES-AMT",
 "CP606190","0400-PROCESS",1163,"WS-*-SALES-AMT per scheme",
 "The same five-scheme shape repeats for returns, loyalty points and rebate discount."),

("SET-02","Merchant volume & settlement","Rebate discount across schemes",
 "Rebate discount totalled the same way across the five schemes.",
 "COMPUTE WS-TOTAL-REB-DISC = WS-VS-REB-DISC + WS-MC-REB-DISC\n  + WS-JB-REB-DISC + WS-DB-REB-DISC + WS-CUP-REB-DISC",
 "CP606190","0400-PROCESS",1557,"WS-*-REB-DISC per scheme",""),
]

PROGRAMS_3 = [
 ("AUS301J","Online","Authorisation enquiry variant — available credit at card, customer and corporate level."),
 ("AUS301M","Online","Authorisation enquiry variant — exposure including transfers out."),
 ("BNDCHNR1","Batch","Banded charge / tier rate reporting."),
 ("BNDRCOE1","Batch","Payment behaviour and cost-of-funds reporting."),
 ("CP510171","Batch (bthsrc)","Settlement summary report."),
 ("CP606190","Batch (bthsrc)","Multi-scheme settlement totals (Visa, MasterCard, JCB, debit, UnionPay)."),
 ("CP610850","Batch (bthsrc)","Merchant year-to-date and prior-year sales statistics."),
 ("CP621690","Batch (bthsrc)","Effective MDR by scheme, card type and domain."),
 ("CPD110B","Batch","Back-dated interest recalculation and provisional interest buckets."),
 ("CPM350","Batch","Merchant statement production — non-qualified sales and adjustments."),
 ("CPOPCHM1","Batch","Merchant volume analysis — on-us, outgoing and interchange-eligible splits."),
 ("CPS333","Copybook","Rate setting: retail, cash and sub-bucket rates, and the regulatory min/max clamp. Copied into CPD110."),
 ("CPSMRPT","Batch","Merchant summary reporting — average ticket and income."),
 ("CPU604","Batch","Mass maintenance for the merchant file."),
 ("QMD048","Batch","Acquirer module daily statistics."),
 ("QMR122","Batch","Acquirer module quarterly retail POS reporting."),
]

PARAMETERS_3 = [
 ("CM-RI2-RATE-* / CM-RI3-RATE-*","Cardholder master","Retail sub-bucket 2 and 3 interest rates","Fraction","RATE-03","CPS333"),
 ("CM-CI2-RATE-*","Cardholder master","Cash sub-bucket 2 interest rate","Fraction","RATE-03","CPS333"),
 ("NOT-APPLY-RTL1-ADJ / NOT-APPLY-CASH1-ADJ","Cardholder master","Whether the account's rate adjustment is applied","Flag","RATE-01, RATE-02","CPS333"),
 ("TC-MINMAX-EFF-FLAG","Min/max rate table","Must equal 1 or the whole rate clamp is skipped","Flag","RATE-04","CPS333"),
 ("TC-MINMAX-MIN-RATE / -MAX-RATE","Min/max rate table","Regulatory floor and ceiling applied to every rate band","Fraction","RATE-04","CPS333"),
 ("ABP-INTR-RATE-1 / ABP-INTR-ADJ-1","Account balance process record","Rate in force at the time, for back-dated recalculation","Fraction","INT-20","CPD110B"),
 ("QMTMPT-GLOBAL-RATES","Merchant pricing table","Scheme global rate, before the base rate is netted off","Percent (/100 in code)","MDR-11","CP621690"),
 ("WS-BSE-RTE","Merchant pricing","Base rate netted off the global rate","Percent","MDR-11","CP621690"),
]

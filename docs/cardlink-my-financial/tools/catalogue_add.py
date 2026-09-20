# -*- coding: utf-8 -*-
"""Second tranche — computations found in the 22 additional programs."""

CATALOGUE_2 = [
# ---------------- Easy Payment Plan / instalment (EPD001) ----------------
("EPP-01","Instalment / fixed-term loan","Monthly instalment from item price",
 "The financed item price divided by the number of payment terms gives the monthly instalment.",
 "COMPUTE WS-MERCH-ADJ-AMT ROUNDED = EPT-ITEM-PRICE / EPT-PAY-TERM",
 "EPD001","(merchant adjustment build)",2212,"EPT-ITEM-PRICE, EPT-PAY-TERM",
 "Easy Payment Plan. The merchant adjustment is the subsidy the merchant funds."),

("EPP-02","Instalment / fixed-term loan","Value of the waived months",
 "The monthly amount multiplied by the number of months in the waiver window, inclusive of both ends.",
 "COMPUTE WS-MERCH-ADJ-AMT =\n  WS-MERCH-ADJ-AMT * (EPT-WAIVE-TO-MOS - EPT-WAIVE-FR-MOS + 1)",
 "EPD001","(merchant adjustment build)",2214,"EPT-WAIVE-FR-MOS, EPT-WAIVE-TO-MOS",
 "The +1 makes the range inclusive — months 3 to 6 is four months, not three."),

("EPP-03","Instalment / fixed-term loan","Instalment billed during the interest-free window",
 "Inside the interest-free months the billed amount is the standard instalment less the interest element, so only principal is demanded.",
 "IF EPT-INTR-FREE-MOS > 0\n  IF EPT-PAID-TERMS > EPT-INTR-FREE-MOS\n    MOVE EPT-MON-INSTL-AMT TO EPGTF-TRANS-AMOUNT\n  ELSE IF EPT-PAID-TERMS = 1\n    MOVE EPT-FIRST-PAY-AMT TO EPGTF-TRANS-AMOUNT\n  ELSE\n    COMPUTE EPGTF-TRANS-AMOUNT = EPT-MON-INSTL-AMT - WS-INTEREST-TEMP",
 "EPD001","0231-CONTINUE",2352,"EPT-INTR-FREE-MOS, EPT-PAID-TERMS, EPT-MON-INSTL-AMT",
 "The first instalment uses EPT-FIRST-PAY-AMT, which may differ from later ones."),

("EPP-04","Instalment / fixed-term loan","Principal portion of an instalment",
 "The instalment less its interest element is the principal repaid this month.",
 "COMPUTE EPGTF-PRIN-AMOUNT = EPGTF-TRANS-AMOUNT - WS-INTEREST",
 "EPD001","0231-CONTINUE",2363,"WS-INTEREST",
 "Standard amortisation split: interest first, the rest reduces principal."),

("EPP-05","Instalment / fixed-term loan","Amortise the outstanding balances",
 "Outstanding principal is reduced by the principal repaid, and outstanding interest by the interest taken.",
 "COMPUTE EPT-OUTS-PRINCIPAL = EPT-OUTS-PRINCIPAL - EPGTF-PRIN-AMOUNT\nSUBTRACT WS-INTEREST FROM EPT-OUTS-INT",
 "EPD001","0231-CONTINUE",2365,"EPT-OUTS-PRINCIPAL, EPT-OUTS-INT",
 "Principal and interest are tracked as separate outstanding balances throughout the plan."),

("EPP-06","Instalment / fixed-term loan","Early settlement amount",
 "Settling early demands the whole outstanding principal plus the outstanding interest.",
 "COMPUTE EPGTF-TRANS-AMOUNT = EPT-OUTS-PRINCIPAL + EPT-OUTS-INT",
 "EPD001","0231-CONTINUE",2306,"EPT-OUTS-PRINCIPAL, EPT-OUTS-INT",
 "Whether unearned interest is rebated is a product decision, not visible in this statement alone."),

# ---------------- Payment allocation (CPS515) ----------------
("PAY-01","Payment allocation","Retail share of a payment",
 "When a payment must be split across retail and cash, the retail share is retail's proportion of the two statement balances.",
 "COMPUTE WS-TEMP-RATE ROUNDED =\n  WS-RTL-STMT-BAL / (WS-CASH-STMT-BAL + WS-RTL-STMT-BAL)",
 "CPS515","PYMT-METHOD-03",203,"WS-RTL-STMT-BAL, WS-CASH-STMT-BAL",
 "Only applied when both balances are above zero; otherwise the payment goes wholly to the non-zero side."),

("PAY-02","Payment allocation","Apply the retail share",
 "The payment multiplied by the retail proportion is posted to retail.",
 "MOVE WS-PYMT TO WS-SAVE-PYMT\nCOMPUTE WS-PYMT ROUNDED = WS-SAVE-PYMT * WS-TEMP-RATE",
 "CPS515","PYMT-METHOD-03",207,"WS-TEMP-RATE",""),

("PAY-03","Payment allocation","Remainder goes to cash",
 "Whatever is left after the retail share is posted to the cash balance, so nothing is lost to rounding.",
 "COMPUTE WS-SAVE-PYMT = WS-SAVE-PYMT - WS-PYMT\nPERFORM PPT-RTL-STMT-BAL\nMOVE WS-SAVE-PYMT TO WS-PYMT\nPERFORM PPT-CASH-STMT-BAL",
 "CPS515","PYMT-METHOD-03",209,"WS-SAVE-PYMT",
 "Taking the remainder rather than a second multiplication is what keeps the two halves summing to the payment."),

("PAY-04","Payment allocation","Split against current-month balances",
 "The same proportional split, applied to current-month balances when the payment exceeds the statement balances.",
 "COMPUTE WS-TEMP-RATE ROUNDED =\n  CM-RTL-CURR-MON-BAL / (CM-CASH-CURR-MON-BAL + CM-RTL-CURR-MON-BAL)",
 "CPS515","PYMT-METHOD-04",222,"CM-RTL-CURR-MON-BAL, CM-CASH-CURR-MON-BAL",
 "Statement balances are cleared first, then current-month balances."),

# ---------------- Interest bucket reconciliation (CPD810) ----------------
("REC-01","Reconciliation & control","Accrued interest bucket roll-forward",
 "Opening balance plus transfers in and accruals and debit adjustments, less transfers out, credit adjustments and waivers, gives the closing bucket.",
 "COMPUTE TCAI-ENDING-BALANCE (IAI) =\n  TCAI-BEG-BALANCE (IAI) + TCAI-TRANSFER-IN (IAI)\n  - TCAI-TRANSFER-OUT (IAI) + TCAI-ACCRUED (IAI)\n  + TCAI-DEBIT-ADJUST (IAI) - TCAI-CREDIT-ADJUST (IAI) - ...",
 "CPD810","KA040-ACCUM-ENDING-BALS",1816,"TCAI-* buckets",
 "CPD810 merges CPD110's updates into CPQAF. A parallel set of CO- fields tracks charged-off accounts."),

("REC-02","Reconciliation & control","Provisional interest bucket roll-forward",
 "The same roll-forward for suspended (provisional) interest, including movements to anticipated and waivers.",
 "COMPUTE TCPI-ENDING-BALANCE = TCPI-BEG-BALANCE + TCPI-ACCRUED\n  - TCPI-NEG-ACCRUED + TCPI-TRANSFER-IN - TCPI-TO-ANTICI\n  - TCPI-WAIVED + TCPI-NEG-WAIVED - TCPI-TRANSFER-OUT",
 "CPD810","KC010-ACCUM-END-PROV-BALS",2018,"TCPI-* buckets",""),

("REC-03","Reconciliation & control","Bucket variance check",
 "The independently accumulated total is compared with the rolled-forward bucket; a non-zero difference is the control break.",
 "COMPUTE WS-AMNT =\n  WST-ENDING-ACCRUED (WS-TA-IDX) - TCAI-ENDING-BALANCE (IAI)",
 "CPD810","KA050-COMPARE-END-BALS",1907,"WST-ENDING-ACCRUED",
 "This is the out-of-balance detector for interest. A non-zero result is what an operator investigates."),

("REC-04","Reconciliation & control","Portfolio balance roll-forward",
 "Organisation-level closing balance: opening plus interest and transfers in and debits, less transfers out, charge-offs and credits.",
 "COMPUTE WS-WORK-AMT = WS-ORG-BEG-BAL + WS-ORG-INTEREST\n  + WS-ORG-TRNSF-IN - WS-ORG-TRNSF-OUT - WS-REG-CHGOFFS\n  + WS-TOT-AMT-DB - WS-TOT-AMT-CR",
 "CPU580","4499-OT-BAL-TOTALS",2774,"WS-ORG-* accumulators",""),

("REC-05","Reconciliation & control","Charged-off portfolio roll-forward",
 "The same roll-forward on the charged-off side, where charge-offs add to rather than reduce the balance.",
 "COMPUTE WS-CO-WORK-AMT = WS-CO-ORG-BEG-BAL + WS-CO-ORG-INTEREST\n  + WS-CO-CHGOFFS + WS-CO-TOT-AMT-DB + WS-CO-ORG-TRNSF-IN\n  - WS-CO-ORG-TRNSF-OUT - WS-CO-TOT-AMT-CR",
 "CPU580","4499-OT-BAL-TOTALS",2788,"WS-CO-* accumulators",
 "Note the sign on charge-offs is opposite to the regular portfolio — they move balance between the two."),

# ---------------- Scheme settlement GL (CP615100 / CP615110) ----------------
("GL-06","Provision & charge-off","Acquiring fee aggregation for GL",
 "Purchase, quasi-cash and chargeback fees are netted into one posting amount per GL category.",
 "COMPUTE WS-TOT-AMT = WS-LOC-ACQ-PURC-FEE + WS-LOC-ACQ-QUASI-FEE\n  + WS-LOC-ACQ-CB-FEE + WS-LOC-ACQ-QUASI-CB-FEE\n  - WS-LOC-ACQ-CB-R-FEE - WS-LOC-ACQ-QUASI-CB-R-FEE",
 "CP615100","(GL category build)",2422,"WS-LOC-ACQ-* fee buckets",
 "LOC = local, INT = international; ACQ = acquiring, ISS = issuing. CB-R is chargeback reversal."),

("GL-07","Provision & charge-off","Scale the GL amount to posting currency",
 "The settlement amount is rescaled by ten to the power of the posting currency's exponent before it is written to the GL.",
 "COMPUTE WS-TOT-AMT = (WS-TOT-AMT * (10 ** CSNGL-GL-POST-CURR-EXP))",
 "CP615100","5100-WRITE-GL-ENTRY",2885,"CSNGL-GL-POST-CURR-EXP",
 "Same mechanism in CP615110. Lets one GL interface serve currencies with different decimal places."),

("GL-08","Provision & charge-off","Acquiring settlement total",
 "Purchases, quasi-cash, manual and reversal amounts netted against returns for the GL entry.",
 "COMPUTE WS-TOT-AMT = WS-LOC-ACQ-PURC + WS-LOC-ACQ-QUASI\n  + WS-LOC-ACQ-MANUAL + WS-LOC-ACQ-PURC-REV-RTN\n  - WS-LOC-ACQ-PURC-RTN",
 "CP615100","5000-GEN-GL-ENTRY",1599,"WS-LOC-ACQ-* amount buckets",""),

# ---------------- Currency ----------------
("FX-03","Currency conversion","Minor units to major units",
 "Scheme files carry amounts in minor units (cents); multiplying by 0.01 converts them to the major unit before reporting.",
 "COMPUTE MERCON-VI-AMT-NET-SALES (1) =\n  MERCON-VI-AMT-NET-SALES (1) * 0.01",
 "CP603160","4950-CONVERT-TO-DECIMAL",1875,"(scheme amount fields)",
 "Applied field by field across every scheme and amount category — 120 such statements in this program alone."),

("FX-04","Currency conversion","Cashback scaled by transaction currency",
 "Cashback is divided by ten to the power of the transaction currency's exponent, or by 100 where no exponent applies.",
 "COMPUTE CXSTX-D-CASHBACK-AMT = WS-ADD-AMT / (10 ** CXS120-TXN-CCY-EXP)\n(else) COMPUTE CXSTX-D-CASHBACK-AMT = WS-ADD-AMT / 100",
 "CXPI040","(cashback build)",4476,"CXS120-TXN-CCY-EXP",""),

# ---------------- Rebate ----------------
("RWD-05","Rewards & rebate","Cash rebate at a flat rate",
 "A flat one percent of the transaction amount is credited as cash rebate.",
 "COMPUTE WS-CASH-REBATE ROUNDED = LF-OUTPUT-AMOUNT * 0.0100",
 "CP621660","4000-FORMAT-PDB-REC",1837,"LF-OUTPUT-AMOUNT",
 "The 0.0100 rate is hard-coded in this program rather than table-driven — worth noting for any rate change."),

("RWD-06","Rewards & rebate","MDR rebate sign",
 "The merchant discount rebate is negated for the output record, expressing it as a credit.",
 "COMPUTE LF-OUTPUT-MDR-REBATE = LF-OUTPUT-MDR-REBATE * -1",
 "CP621660","4000-FORMAT-PDB-REC",1833,"LF-OUTPUT-MDR-REBATE",""),

# ---------------- Mass maintenance (CPU601 / CPU600) ----------------
("MNT-01","Mass maintenance","Percentage increase factor",
 "A percentage increase is turned into a multiplier by dividing by 100 and adding one, then applied to the current value.",
 "COMPUTE WS-PERCENT-HOLD = (WSCPS-MAINT-FIELD-NUMERIC-R (WS-MAINT) / 100) + 1\nCOMPUTE FM1-NH-01-CREDIT-LIMIT = CUR-AMOUNT-OUT * WS-PERCENT-HOLD",
 "CPU601","4200-FILL-FM-01",3379,"WSCPS-MAINT-FIELD-NUMERIC-R",
 "A 10% rise becomes a multiplier of 1.10. This is how bulk limit and rate changes are applied."),

("MNT-02","Mass maintenance","Percentage decrease factor",
 "A percentage decrease becomes one minus the fraction.",
 "COMPUTE WS-PERCENT-HOLD = 1 - (WSCPS-MAINT-FIELD-NUMERIC-R (WS-MAINT) / 100)",
 "CPU601","4200-FILL-FM-01",3388,"WSCPS-MAINT-FIELD-NUMERIC-R",""),

("MNT-03","Mass maintenance","Absolute increase or decrease",
 "Where the change is an amount rather than a percentage it is simply added to or subtracted from the current value.",
 "COMPUTE FM1-NH-01-CREDIT-LIMIT =\n  CUR-AMOUNT-OUT + WSCPS-MAINT-FIELD-NUMERIC-R (WS-MAINT)\n(or - for a decrease)",
 "CPU601","4200-FILL-FM-01",3402,"WSCPS-MAINT-FIELD-NUMERIC-R",""),

# ---------------- Authorisation ----------------
("AUT-01","Credit limit & availability","Available credit at authorisation",
 "During an authorisation enquiry the instalment share of the requested amount is deducted from available credit before the decision.",
 "COMPUTE CM-AVAIL-CREDIT ROUNDED = CM-AVAIL-CREDIT\n  - (AUIS-INQ-AMOUNT-SAVE-AREA * SEC-TC-INSTL-EM-AVL-PER)",
 "AUS301V","(authorisation enquiry)",3910,"AUIS-INQ-AMOUNT-SAVE-AREA, TC-INSTL-EM-AVL-PER",
 "Parallel forms exist for customer level (CR-AVAIL-CREDIT) and corporate level (CORP-CR-AVAIL-CREDIT)."),

("AUT-02","Credit limit & availability","Release the reserve after the decision",
 "The same instalment reserve is added back once the enquiry amount no longer applies.",
 "COMPUTE CM-AVAIL-CREDIT ROUNDED = CM-AVAIL-CREDIT\n  + (AUIS-INQ-AMOUNT-SAVE-AREA * TC-INSTL-EM-AVL-PER)",
 "AUS301V","(authorisation enquiry)",8531,"AUIS-INQ-AMOUNT-SAVE-AREA",""),

# ---------------- Merchant statistics ----------------
("STA-01","Merchant volume & statistics","Average ticket size",
 "Sales amount divided by sales count gives the average ticket, computed separately for international, domestic and out-of-scheme.",
 "COMPUTE QMMRSTA-SLE-ITL-TKT (1) =\n  QMMRSTA-SLE-ITL-AMT (1) / QMMRSTA-SLE-ITL-NBR (1)",
 "QMD045","(merchant statistics)",288,"QMMRSTA-SLE-*-AMT, -NBR",
 "Each divide is guarded by a non-zero count test."),

("STA-02","Merchant volume & statistics","Total sales across channels",
 "Daily international, domestic and out-of-scheme amounts summed to the total.",
 "COMPUTE QMMRSTA-SLE-TTL-AMT (1) =\n  (QMMSTAT-DLY-ITL-AMT + QMMSTAT-DLY-DOM-AMT + QMMSTAT-DLY-OUS-AMT)",
 "QMD045","(merchant statistics)",325,"QMMSTAT-DLY-* amounts",""),

("STA-03","Merchant volume & statistics","Repayment as a percentage of balance",
 "The payment received expressed as a percentage of the current balance.",
 "COMPUTE WS-REPAY-PERCENT ROUNDED =\n  (BNSTRN-AMT / BNS105-CURR-BALANCE (2)) * 100",
 "BNDPAYE1","3000-CALC-REPAY-PERCENT",538,"BNSTRN-AMT, BNS105-CURR-BALANCE",
 "Used to classify payment behaviour — full, partial or minimum payer."),

("MDR-09","Merchant discount (MDR)","Fee-based sales",
 "Sales less returns (or plus returns, depending on how the product treats refunds) gives the base the discount is charged on.",
 "COMPUTE WS-AMT-FEE-BASED-SALES =\n  MPL-PL-AMT-TOTAL-SALES (2) - MPL-PL-AMT-TOTAL-RETURNS (2)\n(or + MPL-PL-AMT-TOTAL-RETURNS (2))",
 "CPM322","3000-COMPUTE-FEE-BASED-SALES",453,"MPL-PL-AMT-TOTAL-SALES, -RETURNS",
 "Whether returns reduce or add to the fee base is a configured choice, and it changes what the merchant pays."),

("MDR-10","Merchant discount (MDR)","Local fee-based sales",
 "Outgoing (non-local) sales are removed so that local and international volumes can be priced differently.",
 "COMPUTE WS-AMT-LOCAL-FEE-BASED-SALE =\n  (MPL-PL-AMT-TOTAL-SALES (2) - MPL-PL-AMT-OUTGO-SALES (2))\n  - (MPL-PL-AMT-TOTAL-RETURNS (2) - MPL-PL-AMT-OUTGO-RETURNS (2))",
 "CPM322","3000-COMPUTE-FEE-BASED-SALES",500,"MPL-PL-AMT-OUTGO-SALES",""),
]

PROGRAMS_2 = [
 ("AUS301V","Online","Authorisation enquiry — available credit and exposure at card, customer and corporate level."),
 ("BNDPAYE1","Batch","Payment behaviour analysis — repayment percentage against balance."),
 ("CP603160","Batch (bthsrc)","Merchant consolidation — converts scheme amounts from minor units to major units."),
 ("CP606370","Batch (bthsrc)","Scheme settlement extract."),
 ("CP614110","Batch (bthsrc)","Scheme settlement extract."),
 ("CP615100","Batch (bthsrc)","Scheme settlement general-ledger posting — acquiring and issuing fee categories."),
 ("CP615110","Batch (bthsrc)","Scheme settlement general-ledger posting — companion to CP615100."),
 ("CP621660","Batch (bthsrc)","Cash rebate and MDR rebate output file."),
 ("CPD110QT","Batch","Quarterly variant of the CPD110 cardholder cycle."),
 ("CPD810","Batch","Interest bucket reconciliation — rolls forward and proves the accrued and provisional interest buckets."),
 ("CPM322","Batch","Private label merchant discount — fee-based sales computation."),
 ("CPM360","Batch","Merchant fee processing."),
 ("CPS515","Batch","Payment allocation — splits a payment across retail and cash balances."),
 ("CPU580","Batch","Organisation and portfolio balance roll-forward reporting."),
 ("CPU601","Batch","Mass maintenance — percentage and absolute changes to limits, rates and user amounts."),
 ("CSM08","Batch (bthsrc)","Scheme settlement processing."),
 ("CXPI040","Batch","Scheme incoming processing — cashback and currency scaling."),
 ("CXU042","Batch","Scheme file utility processing."),
 ("EPD001","Batch","Easy Payment Plan — instalment amortisation, interest-free handling and early settlement."),
 ("QMD032","Batch","Acquirer module daily reporting."),
 ("QMD045","Batch","Merchant statistics — volumes and average ticket size."),
 ("QMR124","Batch","Acquirer module batch reporting."),
]

PARAMETERS_2 = [
 ("EPT-PAY-TERM","EPP plan record","Number of monthly instalments","Months","EPP-01","EPD001"),
 ("EPT-ITEM-PRICE","EPP plan record","Financed item price","Amount","EPP-01","EPD001"),
 ("EPT-INTR-FREE-MOS","EPP plan record","Interest-free months at the start of the plan","Months","EPP-03","EPD001"),
 ("EPT-MON-INSTL-AMT","EPP plan record","Standard monthly instalment","Amount","EPP-03","EPD001"),
 ("EPT-FIRST-PAY-AMT","EPP plan record","First instalment, where it differs from the rest","Amount","EPP-03","EPD001"),
 ("EPT-WAIVE-FR-MOS / -TO-MOS","EPP plan record","Waiver window, inclusive of both months","Months","EPP-02","EPD001"),
 ("CSNGL-GL-POST-CURR-EXP","GL interface record","Posting currency decimal exponent","Exponent","GL-07","CP615100"),
 ("CXS120-TXN-CCY-EXP","Scheme transaction record","Transaction currency decimal exponent","Exponent","FX-04","CXPI040"),
 ("WSCPS-MAINT-FIELD-NUMERIC-R","Mass maintenance request","Percentage or absolute change to apply","Percent or amount","MNT-01, MNT-02, MNT-03","CPU601"),
 ("SEC-TC-INSTL-EM-AVL-PER","Authorisation control","Instalment reserve percentage used at authorisation","Fraction","AUT-01","AUS301V"),
 ("(hard-coded) 0.0100","CP621660 source","Cash rebate rate — held in code, not in a table","Fraction","RWD-05","CP621660"),
]

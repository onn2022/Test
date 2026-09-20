# -*- coding: utf-8 -*-
"""Simplified catalogue of Cardlink MY financial computations.
Every row is evidence-backed: Program / Paragraph / Line point at the real source member."""

# id, domain, what it computes, plain-English rule, COBOL as written, program, paragraph, line, drivers, notes
CATALOGUE = [
# ---------------- A. Interest ----------------
("INT-01","Interest — finance charge","Daily interest fraction (day factor)",
 "An annual rate is turned into a daily one. The divisor depends on the year basis set for the product: 360, 365, or 366 in a leap year.",
 "IF YEAR-BASE-360  MOVE .0027778 TO WSI-DAY-FACTOR\nIF YEAR-BASE-365  MOVE .0027397 TO WSI-DAY-FACTOR\nIF YEAR-BASE-366  MOVE .0027322 (leap) / .0027397 TO WSI-DAY-FACTOR",
 "CPD110","COMPUTE-DAY-FACTOR",13209,"YEAR-BASE-360 / 365 / 366",
 ".0027778 = 1/360, .0027397 = 1/365, .0027322 = 1/366. Leap year is tested from OC-TODAYS-JULIAN."),

("INT-02","Interest — finance charge","Number of days to accrue",
 "Days between the date interest was last accrued through and the new accrue-through date.",
 "MOVE CM-DTE-ACCR-THRU TO WS-DTE-DATE-2\nMOVE WS-ACCR-THRU-DTE TO WS-DTE-DATE-1\nPERFORM ZZZZ-ELAPSED-DAYS -> WS-DTE-RESULT\nMOVE WS-DTE-RESULT TO WSI-DAYS",
 "CPD110","PROCESS-INTEREST-RATE",11600,"CM-DTE-ACCR-THRU, WS-ACCR-THRU-DTE",
 "Drives every accrual below. CM-DTE-LST-ACCR keeps the previous value for audit."),

("INT-03","Interest — finance charge","One day's interest — single rate",
 "Balance x annual rate x daily fraction. This is the base case when the product has no rate bands.",
 "COMPUTE WSI-ACCRUAL ROUNDED = WSI-AMNT * WSI-RATE-1 * WSI-DAY-FACTOR",
 "CPD110","INTEREST-PROCESSING",13982,"WSI-AMNT, WSI-RATE-1, WSI-DAY-FACTOR",
 "WSI-AMNT is the interest-bearing balance for the bucket being processed (cash or retail)."),

("INT-04","Interest — finance charge","One day's interest — two rate bands",
 "The balance up to the first limit is charged at rate 1; everything above it at rate 2.",
 "COMPUTE WSI-ACCRUAL ROUNDED =\n  (WSI-LIMIT-1 * WSI-RATE-1\n   + (WSI-AMNT - WSI-LIMIT-1) * WSI-RATE-2) * WSI-DAY-FACTOR",
 "CPD110","INTEREST-PROCESSING",13989,"WSI-LIMIT-1, WSI-RATE-1, WSI-RATE-2",
 "Tiered pricing. Applied when the balance exceeds WSI-LIMIT-1 but not WSI-LIMIT-2."),

("INT-05","Interest — finance charge","One day's interest — three rate bands",
 "Band 1 up to limit 1 at rate 1, band 2 between the two limits at rate 2, the remainder at rate 3.",
 "COMPUTE WSI-ACCRUAL ROUNDED =\n  (WSI-LIMIT-1 * WSI-RATE-1\n   + (WSI-LIMIT-2 - WSI-LIMIT-1) * WSI-RATE-2\n   + (WSI-AMNT - WSI-LIMIT-2) * WSI-RATE-3) * WSI-DAY-FACTOR",
 "CPD110","INTEREST-PROCESSING",13993,"WSI-LIMIT-1, WSI-LIMIT-2, WSI-RATE-1/2/3",
 "Full three-tier ladder — the most general interest shape in the MY portfolio."),

("INT-06","Interest — finance charge","One day's interest — flat top rate",
 "Whole balance charged at rate 3, used where the product prices everything at the top band.",
 "COMPUTE WSI-ACCRUAL ROUNDED = WSI-AMNT * WSI-RATE-3 * WSI-DAY-FACTOR",
 "CPD110","INTEREST-PROCESSING",14003,"WSI-AMNT, WSI-RATE-3","Terminal branch of the banding logic."),

("INT-07","Interest — finance charge","Scale one day's interest to the period",
 "One day's interest multiplied by the number of days since the last accrual.",
 "MULTIPLY WSI-DAYS BY WSI-ACCRUAL\n(also: COMPUTE WSI-ACCRUAL ROUNDED = WSI-ACCRUAL * WSI-DAYS)",
 "CPD110","INTEREST-PROCESSING",12472,"WSI-DAYS",
 "Simple (not compound) interest: the per-diem is not re-based within the period."),

("INT-08","Interest — finance charge","Total across bands",
 "The three band accruals are added into one figure for the bucket.",
 "COMPUTE WSI-ACCRUAL = WSI-ACCRUAL-1 + WSI-ACCRUAL-2 + WSI-ACCRUAL-3",
 "CPD110","INTEREST-PROCESSING",13960,"WSI-ACCRUAL-1/2/3",""),

("INT-09","Interest — finance charge","Post accrual to the cash bucket",
 "Accrued cash interest is added to the account's cash interest bucket and to the daily interest-accrual record.",
 "ADD WSI-ACCRUAL TO CM-CASH-ACCRUED-INTR\nADD WSI-ACCRUAL TO INTM-INTACR-CSH-ACCRUED-TODAY",
 "CPD110","INTEREST-PROCESSING",12486,"CM-CASH-ACCRUED-INTR",
 "Cash and retail interest are accrued and held separately all the way to statement."),

("INT-10","Interest — finance charge","Post accrual to the retail bucket",
 "Accrued retail interest is added to the account's retail interest bucket.",
 "ADD WSI-ACCRUAL TO CM-RTL-ACCRUED-INTR\nADD WSI-ACCRUAL TO INTM-INTACR-RTL-ACCRUED-TODAY",
 "CPD110","INTEREST-PROCESSING",12738,"CM-RTL-ACCRUED-INTR",""),

("INT-11","Interest — finance charge","Which buckets accrue at all",
 "Cash interest is calculated only when the cash balance is positive and the account is not cash-interest-free; the same test applies to retail.",
 "IF CASH-INTR-FREE AND CASH2-INTR-FREE  NEXT SENTENCE\nELSE IF CM-CASH-BALANCE > ZERO  PERFORM COMPUTE-CASH-INTEREST\nIF RETAIL-INTR-FREE AND RETAIL2/3-INTR-FREE  NEXT SENTENCE\nELSE IF CM-RTL-BALANCE > ZERO  PERFORM COMPUTE-RETAIL-INTEREST",
 "CPD110","COMPUTE-INTEREST-ACCRUAL",12226,"CASH-INTR-FREE, RETAIL-INTR-FREE",
 "Interest-free (grace) status is per sub-bucket, not per account."),

("INT-12","Interest — finance charge","Whole-account interest freeze",
 "If the account is frozen for interest, or every bucket is interest-free, accrual is skipped entirely for the day.",
 "IF FREEZE-INTEREST (IBC) OR (CASH-INTR-FREE AND CASH2-INTR-FREE AND\n   RETAIL-INTR-FREE AND RETAIL2-INTR-FREE AND RETAIL3-INTR-FREE)\n   PERFORM UPDATE-ACCT-ANTICIPATE-DATE ... GO TO PIR-XIT-1",
 "CPD110","PROCESS-INTEREST-RATE",11618,"FREEZE-INTEREST (IBC)",
 "The accrue-through date still rolls forward, so no days are double-counted later."),

("INT-13","Interest — finance charge","Effective rate = base + adjustment",
 "The rate actually applied is the product rate plus any account-level adjustment; x100 turns it into a displayable percentage.",
 "COMPUTE WSM-CBC-RATE ROUNDED = (CM-CI-RATE-1 + CM-CI-ADJ-1) * 100\nCOMPUTE WSM-CAC-RATE ROUNDED = CM-CI-RATE-2 * 100",
 "CPD110","INTEREST-PROCESSING",11686,"CM-CI-RATE-1..3, CM-CI-ADJ-1..3, CM-RI-RATE-1..3, CM-RI-ADJ-1..3",
 "CI- = cash interest, RI- = retail interest. Rates are held as decimal fractions."),

("INT-14","Interest — finance charge","Total accrued interest on the account",
 "All five interest buckets added together for reporting and for the available-credit reduction.",
 "COMPUTE WS-WORK-ACCRUED-INT = CM-RTL-ACCRUED-INTR + CM-RTL2-ACCRUED-INTR\n  + CM-RTL3-ACCRUED-INTR + CM-CASH-ACCRUED-INTR + CM-CASH2-ACCRUED-INTR",
 "CPD110","CARDHOLDER-PROCESSING",5712,"CM-RTL/CASH-ACCRUED-INTR",""),

("INT-15","Interest — finance charge","Average daily balance accumulator",
 "Balance multiplied by days is accumulated each cycle; dividing the total by the accumulated days gives the average daily balance.",
 "COMPUTE CM-AGGR-YTD-BALANCE = CM-AGGR-YTD-BALANCE\n  + ((CM-CASH-BALANCE + CM-RTL-BALANCE) * WSI-DAYS)\nADD WSI-DAYS TO CM-AGGR-YTD-DAYS",
 "CPD110","PROCESS-INTEREST-RATE",11615,"CM-AGGR-YTD-BALANCE, CM-AGGR-YTD-DAYS",
 "Parallel cash-only and retail-only counters exist (CM-AGGR-CASH-DAYS, CM-AGGR-RTL-DAYS)."),

("INT-16","Interest — finance charge","Interest earned on a credit balance",
 "When the account is in credit, interest is paid to the customer: balance x credit rate x daily fraction x days. "
 "The balance is first capped at limit 3, then rate 1 or rate 2 applies depending on whether it is below limit 2.",
 "IF WSI-AMNT > TCICB-LIMIT-3  MOVE TCICB-LIMIT-3 TO WSI-AMNT\nIF WSI-AMNT < TCICB-LIMIT-2\n  COMPUTE CM-IE-ACCRUED ROUNDED =\n    WSI-AMNT * TCICB-RATE-1 * WSI-DAY-FACTOR * CM-IE-AGGR-DAYS\nELSE\n  COMPUTE CM-IE-ACCRUED ROUNDED =\n    WSI-AMNT * TCICB-RATE-2 * WSI-DAY-FACTOR * CM-IE-AGGR-DAYS",
 "CPD110","STATEMENT-PREPARATION",15489,"TCICB-RATE-1/2, TCICB-LIMIT-2/3, CM-IE-AGGR-DAYS",
 "TCICB = interest on credit balance. The cap at limit 3 means credit interest is not paid on very large credit balances."),

("INT-17","Interest — finance charge","Reverse accrued interest (waiver / early settlement)",
 "An accrual already taken is subtracted back out of the bucket and out of the daily accrual record.",
 "SUBTRACT WSI-ACCRUAL FROM CM-CASH-ACCRUED-INTR\nSUBTRACT WSI-ACCRUAL FROM CM-RTL-ACCRUED-INTR",
 "CPD110","TRANSACTION-PROCESSING",9561,"WSI-ACCRUAL",
 "Used when a payment back-dates into the accrual period, or interest is waived."),

("INT-18","Interest — finance charge","Anticipated interest net of negative anticipation",
 "Retail interest expected to be billed, less interest already anticipated in the other direction.",
 "COMPUTE WSI-ACCRUAL-RTL = CM-RTL-ACCRUED-INTR - CM-RTL-NEG-ANTICI-INTR",
 "CPD110","TRANSACTION-PROCESSING",9610,"CM-RTL-NEG-ANTICI-INTR",
 "Source comment notes negative anticipated balances became redundant from V2R1 onward."),

("INT-19","Interest — finance charge","Back-dated transaction interest",
 "Interest on a single back-dated transaction: its amount x rate x daily fraction.",
 "COMPUTE WSI-ACCRUAL ROUNDED = CMT-AMNT * WSI-RATE * WSI-DAY-FACTOR",
 "CPD110","INTEREST-PROCESSING",14655,"CMT-AMNT, WSI-RATE",""),

# ---------------- B. Cash advance fee ----------------
("CAF-01","Cash advance fee","Pick the fee rate row",
 "The cash-advance fee table is searched on the transaction's source code. ATM network names map to fixed source codes.",
 "MOVE CMT-SOURCE-CODE TO WS-SOURCE-CODE  (or CMT-ORIG-SOURCE-CODE if transferred)\nIF WS-SHORT-DESC = 'CIRRUS'  MOVE +0015 TO WS-SOURCE-CODE\nIF WS-SHORT-DESC = 'PLUS  '  MOVE +0014 TO WS-SOURCE-CODE\nSEARCH TC-CA-PER-TABLE WHEN TC-CA-PER-SRCE (ICAP) = WS-SOURCE-CODE",
 "CPD110","CASH-ADV-PERCENT-CHARGE",28825,"TC-CA-PER-SRCE, CMT-SOURCE-CODE",
 "No matching row means no percentage fee is raised (AT END GO TO CAPC-EXIT)."),

("CAF-02","Cash advance fee","Single-rate fee (no band limit)",
 "Where the table row has no limit, the fee is simply a percentage of the advance.",
 "COMPUTE WS-CA-PERCENT-CHARGE ROUNDED =\n  (CMT-AMNT * TC-CA-PER-RATE-1 (ICAP)) / 100",
 "CPD110","CAPC-NO-LIMIT",28850,"TC-CA-PER-RATE-1",
 "Divide by 100 because the table holds the rate as a percentage, not a fraction."),

("CAF-03","Cash advance fee","Banded fee — amount within the limit",
 "If the advance is not above the band limit, rate 1 applies to the whole amount.",
 "IF CMT-AMNT NOT > TC-CA-PER-LIMIT (ICAP)\n  COMPUTE WS-CA-PERCENT-CHARGE ROUNDED =\n    (CMT-AMNT * TC-CA-PER-RATE-1 (ICAP)) / 100",
 "CPD110","CAPC-TWO-RATES",28855,"TC-CA-PER-LIMIT, TC-CA-PER-RATE-1",""),

("CAF-04","Cash advance fee","Banded fee — amount above the limit",
 "Above the limit the fee is split: rate 1 on the limit, rate 2 on the excess.",
 "COMPUTE WS-CA-AMNT-OVER-LIMIT = CMT-AMNT - TC-CA-PER-LIMIT (ICAP)\nCOMPUTE WS-CA-PERCENT-CHARGE ROUNDED =\n  ((TC-CA-PER-LIMIT (ICAP) * TC-CA-PER-RATE-1 (ICAP))\n   + (WS-CA-AMNT-OVER-LIMIT * TC-CA-PER-RATE-2 (ICAP))) / 100",
 "CPD110","CAPC-TWO-RATES",28858,"TC-CA-PER-LIMIT, TC-CA-PER-RATE-1, TC-CA-PER-RATE-2",""),

("CAF-05","Cash advance fee","Floor and cap the fee",
 "The computed fee is raised to the minimum charge, or cut to the maximum charge.",
 "IF WS-CA-PERCENT-CHARGE < TC-CA-PERCENT-MIN-CHRG\n  MOVE TC-CA-PERCENT-MIN-CHRG TO WS-CA-PERCENT-CHARGE\nIF WS-CA-PERCENT-CHARGE > TC-CA-PERCENT-MAX-CHRG\n  MOVE TC-CA-PERCENT-MAX-CHRG TO WS-CA-PERCENT-CHARGE",
 "CPD110","CAPC-MIN-MAX",28866,"TC-CA-PERCENT-MIN-CHRG, TC-CA-PERCENT-MAX-CHRG",
 "This is the classic 'x% of the advance, minimum RMn' rule."),

("CAF-06","Cash advance fee","Raise the fee transaction",
 "The fee is posted as its own transaction, into the cash bucket.",
 "PERFORM GENERATE-BASIC-TRANS\nMOVE 3700 TO GT-TRANS-CODE GT-TRANS-TYPE\nMOVE 'CSH1' TO GT-BAL-BUCKET\nMOVE WS-CA-PERCENT-CHARGE TO GT-AMNT",
 "CPD110","CAPC-GEN-TRANS",28873,"GT-TRANS-CODE 3700",
 "Posting to CSH1 means the fee itself then attracts cash-rate interest."),

("CAF-07","Cash advance fee","Cash balance used for authorisation",
 "Cash exposure = posted cash balance plus outstanding cash authorisations, less over-limit payments already credited.",
 "COMPUTE ACR-CM-CASHBAL-AUTH =\n  CM-CASH-BALANCE + CM-CASH-ADV-OS-AUTH - CM-OL-CASH-PYMT",
 "CPD110","9400-CUSTOMER-CALCULATE",29108,"CM-CASH-ADV-OS-AUTH",""),

# ---------------- C. Late charge ----------------
("LATE-01","Late / penalty charge","Balance the late fee is measured on",
 "The late-fee base is the opening (beginning) balance of the cycle, retail plus cash.",
 "COMPUTE CM-STMT-BAL-FOR-LATE-FEE =\n  CM-RTL-BEG-BALANCE + CM-CASH-BEG-BALANCE",
 "CPD110","CARDHOLDER-PROCESSING",5841,"CM-RTL-BEG-BALANCE, CM-CASH-BEG-BALANCE",""),

("LATE-02","Late / penalty charge","Waiver and zero-base guards",
 "No late charge is raised if the account or product waives it. If the base balance is zero or below, the accrued late-charge buckets are cleared.",
 "IF WAIVE-LATE-CHARGES OR TC-WAIVE-LATE-CHRG (IBC)  GO TO LCP-XIT\nIF CM-STMT-BAL-FOR-LATE-FEE <= ZEROS\n  MOVE ZEROES TO CM-ACCR-LATE-CHG-CTD CM-ACCR-LATE-CHG-BNP",
 "CPD110","LATE-CHARGE-PROCESSING",18186,"WAIVE-LATE-CHARGES, TC-WAIVE-LATE-CHRG",""),

("LATE-03","Late / penalty charge","Flat fee plus percentage of unpaid balance (flag 2)",
 "A fixed charge plus a percentage of the unpaid statement balances across all retail, cash and insurance buckets.",
 "COMPUTE WS-AMNT ROUNDED = TCM-LATE-CHARGE +\n  ((CM-RTL1-BALANCE-STMT + CM-CASH1-BALANCE-STMT\n    + CM-RTL2-BALANCE-STMT + CM-CASH2-BALANCE-STMT\n    + CM-RTL3-BALANCE-STMT + CM-RTL-INSUR-BNP) * TCM-LC-PERCENT)",
 "CPD110","LATE-CHARGE-PROCESSING",18219,"TCF-LATE-CHARGE-FLAG=2, TCM-LATE-CHARGE, TCM-LC-PERCENT",""),

("LATE-04","Late / penalty charge","Flat fee only (flag 0 or 5)",
 "A single fixed late charge, regardless of balance.",
 "IF TCF-LATE-CHARGE-FLAG IS EQUAL TO 0 OR 5\n  COMPUTE WS-AMNT ROUNDED = TCM-LATE-CHARGE",
 "CPD110","LATE-CHARGE-PROCESSING",18225,"TCF-LATE-CHARGE-FLAG=0/5, TCM-LATE-CHARGE",""),

("LATE-05","Late / penalty charge","Flat fee plus percentage of total unpaid",
 "Variant that applies the percentage to a single total-unpaid figure.",
 "COMPUTE WS-AMNT ROUNDED =\n  TCM-LATE-CHARGE + (WS-TOT-UNPAID-BAL * TCM-LC-PERCENT)",
 "CPD110","LATE-CHARGE-PROCESSING",18234,"TCM-LATE-CHARGE, TCM-LC-PERCENT",""),

# ---------------- D. Over limit ----------------
("OVL-01","Over-limit","Amount over the credit limit",
 "How far the posted balance exceeds the credit limit.",
 "COMPUTE CPCT-AMT-OVERLIMIT =\n  CM-RTL-BALANCE + CM-CASH-BALANCE - CM-CRLIMIT",
 "CPD110","INPUT-OUTPUT-PROCESSING",23780,"CM-CRLIMIT",""),

("OVL-02","Over-limit","Over-limit amount added to amount due",
 "Any new over-limit excess not already demanded is added to the over-limit amount due.",
 "COMPUTE WS-AMNT = (CM-CURR-BALANCE - CM-CRLIMIT) - CM-OL-AMT-DUE\nCOMPUTE CM-OL-AMT-DUE = CM-OL-AMT-DUE + WS-AMNT",
 "CPD110","STATEMENT-PREPARATION",16260,"CM-OL-AMT-DUE",""),

# ---------------- E. Limits & availability ----------------
("LMT-01","Credit limit & availability","Cash limit derived from credit limit",
 "The cash limit is a set percentage of the overall credit limit.",
 "COMPUTE CM-CASH-LIMIT ROUNDED = TCM-CASH-LIMIT-PERCENT * CM-CRLIMIT",
 "CPD110","CARDHOLDER-PROCESSING",7349,"TCM-CASH-LIMIT-PERCENT, CM-CRLIMIT",""),

("LMT-02","Credit limit & availability","Instalment limit derived from credit limit",
 "The instalment limit is a set percentage of the overall credit limit.",
 "COMPUTE CM-INSTL-LIMIT ROUNDED = TCM-INSTL-LIMIT-PERCENT * CM-CRLIMIT",
 "CPD110","CARDHOLDER-PROCESSING",7351,"TCM-INSTL-LIMIT-PERCENT, CM-CRLIMIT",""),

("LMT-03","Credit limit & availability","Available credit",
 "Limit (grossed up by the permitted over-limit factor) less what is used, less outstanding authorisations, plus over-limit payments received.",
 "COMPUTE CM-AVAIL-CREDIT ROUNDED =\n  (CM-CRLIMIT * TCM-OVER-LIMIT) - CM-CURR-BALANCE\n  - CM-AMNT-OUTST-AUTH + CM-OL-CASH-PYMT + CM-OL-RTL-PYMT",
 "CPD110","CARDHOLDER-PROCESSING",7404,"TCM-OVER-LIMIT, CM-AMNT-OUTST-AUTH",
 "TCM-OVER-LIMIT is a multiplier (e.g. 1.10 for a 10% tolerance), not an amount."),

("LMT-04","Credit limit & availability","Available cash",
 "Cash limit grossed up by the over-limit factor, less cash balance and outstanding cash authorisations.",
 "COMPUTE CM-AVAIL-CASH ROUNDED =\n  CM-CASH-LIMIT * TCM-OVER-LIMIT - CM-CASH-BALANCE\n  - CM-CASH-ADV-OS-AUTH + CM-OL-CASH-PYMT",
 "CPD110","CARDHOLDER-PROCESSING",7375,"TCM-OVER-LIMIT, CM-CASH-ADV-OS-AUTH",""),

("LMT-05","Credit limit & availability","Available instalment limit",
 "Instalment limit less instalment balance and outstanding instalment authorisations.",
 "COMPUTE CM-AVAIL-INSTL ROUNDED =\n  CM-INSTL-LIMIT - CM-INSTL-BAL - CM-AMNT-OUTST-INSTL",
 "CPD110","CARDHOLDER-PROCESSING",7384,"CM-INSTL-BAL, CM-AMNT-OUTST-INSTL",""),

("LMT-06","Credit limit & availability","Instalment balance reserved against available credit",
 "Only a configured share of the instalment balance is held back from the main available credit.",
 "COMPUTE CM-AVAIL-CREDIT =\n  CM-AVAIL-CREDIT - (TC-INSTL-EM-AVL-PER * CM-INSTL-BAL)",
 "CPD110","CARDHOLDER-PROCESSING",7411,"TC-INSTL-EM-AVL-PER",""),

("LMT-07","Credit limit & availability","Available credit net of accrued interest",
 "Unbilled accrued interest is deducted from available credit so the customer cannot spend it.",
 "COMPUTE CM-AVAIL-CREDIT ROUNDED = (WS-AMNT\n  - CM-RTL-ACCRUED-INTR - CM-RTL2-ACCRUED-INTR - CM-RTL3-ACCRUED-INTR\n  - CM-CASH-ACCRUED-INTR - CM-CASH2-ACCRUED-INTR)",
 "CPD110","CARDHOLDER-PROCESSING",7396,"CM-*-ACCRUED-INTR",""),

("LMT-08","Credit limit & availability","Credit limit utilisation",
 "Debits as a proportion of the credit limit, scaled to one decimal place of a percentage.",
 "COMPUTE WS-CREDIT-LIMIT-USG = (WS-USER-AMT-DEBITS / CM-CRLIMIT) * 1000\nCOMPUTE CESF01-CRLIMIT-USG-TODAY = WS-CREDIT-LIMIT-USG / 10",
 "CPD110","CARDHOLDER-PROCESSING",6014,"WS-USER-AMT-DEBITS, CM-CRLIMIT",
 "x1000 then /10 preserves one decimal in integer arithmetic."),

# ---------------- F. Minimum payment ----------------
("MIN-01","Minimum payment / amount due","Bill the whole balance",
 "Where the product bills in full, the amount due is simply the current balance.",
 "IF BILL-TOTAL-BALANCE  MOVE CM-CURR-BALANCE TO WS-PYMT",
 "CPD110","COMPUTE-CURR-PYMT",28297,"BILL-TOTAL-BALANCE",
 "Charge cards and some corporate products use this."),

("MIN-02","Minimum payment / amount due","Bill a fixed amount",
 "A pre-set fixed instalment is billed instead of a percentage.",
 "IF BILL-FIXED-AMNT AND CM-FIXED-PYMT-AMNT > ZERO\n  MOVE CM-FIXED-PYMT-AMNT TO WS-PYMT",
 "CPD110","COMPUTE-CURR-PYMT",28308,"CM-FIXED-PYMT-AMNT",""),

("MIN-03","Minimum payment / amount due","Derive the fixed amount from principal",
 "The fixed payment is a percentage of principal, where principal excludes disputed balances and billed charges.",
 "COMPUTE WS-PRINCIPAL-AMOUNT EQUAL CM-CURR-BALANCE\n  - CM-CASH-DISPUTED-BAL - CM-RTL-DISPUTED-BAL - WS-PRINCIPAL-CHARGES\nCOMPUTE CM-FIXED-PYMT-AMNT ROUNDED EQUAL\n  WS-PRINCIPAL-AMOUNT * TCP-PERCENT (ITCP)",
 "CPD110","SET-NEW-FIXED-PYMT",16543,"TCP-PERCENT",
 "TCP-PERCENT is picked from a table band (ITCP) — high balance, reducing, or new-debit method."),

("MIN-04","Minimum payment / amount due","Interest-only billing",
 "Only interest held plus charges and billed interest fees are demanded.",
 "COMPUTE WS-PYMT = WS-RTL-ACCR-HOLD + WS-CASH-ACCR-HOLD\n  + WS-RTL-CHRG + WS-CASH-CHRG + WS-BILL-INTR-FEES",
 "CPD110","COMPUTE-CURR-PYMT",28314,"BILL-INTEREST-ONLY",""),

("MIN-05","Minimum payment / amount due","Split into bill-in-full and revolving parts",
 "Balances are split: WS-PYMT1 is billed in full (fees, instalment due), WS-PYMT2 is the revolving remainder.",
 "MOVE ZEROES TO WS-PYMT1 WS-PYMT2\nPERFORM BAL-BUCKET-BILL-FULL\nADD CM-CTD-IPP-BALANCE TO WS-PYMT1\nSUBTRACT CM-CTD-IPP-BALANCE FROM WS-PYMT2\nSUBTRACT CM-PCB-IPP-BALANCE FROM WS-PYMT2",
 "CPD110","COMPUTE-CURR-PYMT",28325,"CM-CTD-IPP-BALANCE, CM-PCB-IPP-BALANCE",
 "IPP = instalment payment plan; its current due is always billed in full."),

("MIN-06","Minimum payment / amount due","Revolving part — divisor method",
 "Where the derive method is zero, the revolving part is divided by the payment term.",
 "IF TCM-DERIVE-METHOD = ZERO\n  COMPUTE WS-PYMT ROUNDED = WS-PYMT1 + WS-PYMT2 / TCM-PAYMENT-TERM",
 "CPD110","COMPUTE-CURR-PYMT",28335,"TCM-DERIVE-METHOD=0, TCM-PAYMENT-TERM",
 "E.g. a term of 20 bills 1/20th = 5% of the revolving balance."),

("MIN-07","Minimum payment / amount due","Revolving part — percentage method",
 "Otherwise the revolving part is multiplied by the payment term treated as a percentage.",
 "ELSE\n  COMPUTE WS-PYMT ROUNDED =\n    WS-PYMT1 + WS-PYMT2 * TCM-PAYMENT-TERM / 100",
 "CPD110","COMPUTE-CURR-PYMT",28341,"TCM-DERIVE-METHOD<>0, TCM-PAYMENT-TERM",
 "E.g. a term of 5 bills 5% of the revolving balance."),

("MIN-08","Minimum payment / amount due","Negative revolving part",
 "If the revolving remainder is negative it is added as-is rather than being scaled.",
 "IF WS-PYMT2 < ZERO\n  COMPUTE WS-PYMT = WS-PYMT1 + WS-PYMT2",
 "CPD110","COMPUTE-CURR-PYMT",28331,"WS-PYMT2",""),

("MIN-09","Minimum payment / amount due","Bill the whole balance when no term is set",
 "A zero payment term with a zero derive method means the full balance is demanded.",
 "IF TCM-PAYMENT-TERM = ZERO AND TCM-DERIVE-METHOD = ZERO\n  MOVE CM-CURR-BALANCE TO WS-PYMT",
 "CPD110","COMPUTE-CURR-PYMT",28322,"TCM-PAYMENT-TERM, TCM-DERIVE-METHOD",""),

("MIN-10","Minimum payment / amount due","Apply the minimum payment floor",
 "If the computed amount is below the product minimum, the minimum is used — unless the balance is under the threshold, or the card is interest-only, budget or fixed-term-loan.",
 "IF BILL-INTEREST-ONLY OR CM-CURR-BALANCE NOT > TCM-PYMT-THRESHOLD\n  NEXT SENTENCE\nELSE IF (WS-PYMT < TCM-MINIMUM-PYMT)\n  AND NOT BUDGET-CARD AND NOT FIXED-TERM-LOAN-CARD\n  MOVE TCM-MINIMUM-PYMT TO WS-PYMT",
 "CPD110","COMPUTE-CURR-PYMT",28349,"TCM-MINIMUM-PYMT, TCM-PYMT-THRESHOLD",
 "This is the 'or RMn, whichever is higher' clause on a statement."),

("MIN-11","Minimum payment / amount due","Round up to whole currency units",
 "Where the product bills in even dollars, .99 is added and the result truncated — i.e. rounded up.",
 "IF BILL-EVEN-DOLLARS\n  ADD .99 TO WS-PYMT\n  MOVE WS-PYMT TO WS-DOLLARS\n  MOVE WS-DOLLARS TO WS-PYMT",
 "CPD110","COMPUTE-CURR-PYMT",28356,"BILL-EVEN-DOLLARS",
 "WS-DOLLARS has no decimal places, so the MOVE truncates."),

("MIN-12","Minimum payment / amount due","Add the full over-limit excess",
 "If the balance is over the limit and the product demands all of it, the whole excess is added on top of the minimum.",
 "IF CM-CURR-BALANCE > CM-CRLIMIT AND BILL-ALL-OVER-LIMIT\n  COMPUTE WS-PYMT = WS-PYMT + (CM-CURR-BALANCE - CM-CRLIMIT)",
 "CPD110","COMPUTE-CURR-PYMT",28365,"BILL-ALL-OVER-LIMIT",""),

# ---------------- G. Service / transaction charges ----------------
("SVC-01","Service & transaction charges","Tiered per-transaction charge",
 "Transactions up to the free/banded limit are charged at rate 1, the rest at rate 2.",
 "IF TCSC-LIMIT (ISC) > ZERO AND WS-COUNT > TCSC-LIMIT (ISC)\n  COMPUTE WS-CHRG =\n    (TCSC-LIMIT (ISC) * TCSC-RATE-1 (ISC))\n    + ((WS-COUNT - TCSC-LIMIT (ISC)) * TCSC-RATE-2 (ISC))",
 "CPD110","CALCULATE-TRANS-CHRG",15540,"TCSC-LIMIT, TCSC-RATE-1, TCSC-RATE-2",
 "WS-COUNT is the transaction count for the bucket, not an amount."),

("SVC-02","Service & transaction charges","Flat per-transaction charge",
 "With no band, every transaction is charged at rate 1.",
 "COMPUTE WS-CHRG = WS-COUNT * TCSC-RATE-1 (ISC)",
 "CPD110","CALCULATE-TRANS-CHRG",15551,"TCSC-RATE-1",""),

("SVC-03","Service & transaction charges","Split the charge to retail or cash",
 "The charge lands in the retail or the cash bucket depending on the service-charge type.",
 "IF TSC-RETAIL (ISC)  ADD WS-CHRG TO WS-RTL-CHRG\nELSE  ADD WS-CHRG TO WS-CASH-CHRG",
 "CPD110","CALCULATE-TRANS-CHRG",15556,"TSC-RETAIL",""),

("SVC-04","Service & transaction charges","Cap the total service charge",
 "Retail and cash charges are totalled; if the total breaches the maximum, the bucket currently being processed is cut back "
 "so that the two together equal the cap.",
 "COMPUTE WS-AMNT = WS-RTL-CHRG + WS-CASH-CHRG\nIF (WS-AMNT > TCSC-MAXIMUM)\n  IF (TSC-RETAIL (ISC))\n    COMPUTE WS-RTL-CHRG = TCSC-MAXIMUM - WS-CASH-CHRG\n  ELSE\n    COMPUTE WS-CASH-CHRG = TCSC-MAXIMUM - WS-RTL-CHRG",
 "CPD110","CALCULATE-TRANS-CHRG",15560,"TCSC-MAXIMUM, TSC-RETAIL",
 "The cap is on the combined charge, not per bucket. WS-MAX-TR-SW is set to flag that the cap was hit."),

# ---------------- H. Balances ----------------
("BAL-01","Balances & statement","Current balance",
 "Retail plus cash balances, less amounts under dispute.",
 "COMPUTE CM-CURR-BALANCE = CM-RTL-BALANCE + CM-CASH-BALANCE\n  - CM-RTL-DISPUTED-BAL - CM-CASH-DISPUTED-BAL",
 "CPD110","COMPUTE-CURR-BAL",28272,"CM-RTL-BALANCE, CM-CASH-BALANCE",
 "Disputed amounts are excluded from the balance the customer is asked to pay."),

("BAL-02","Balances & statement","Current balance (pre-dispute form)",
 "A simple retail plus cash total used earlier in the cycle.",
 "COMPUTE CM-CURR-BALANCE = CM-CASH-BALANCE + CM-RTL-BALANCE",
 "CPD110","PA-BYPASS-MEM-USAGE-FEE",5679,"CM-CASH-BALANCE, CM-RTL-BALANCE",""),

("BAL-03","Balances & statement","Retail balance across sub-buckets",
 "The three retail sub-buckets are summed into the retail total.",
 "COMPUTE CM-RTL-CURR-MON-BAL = CM-RTL1-CURR-MON-BAL\n  + CM-RTL2-CURR-MON-BAL + CM-RTL3-CURR-MON-BAL",
 "CPD110","(statement build)",27284,"CM-RTL1/2/3-CURR-MON-BAL",
 "Sub-buckets carry different interest rates, which is why they are held apart."),

("BAL-04","Balances & statement","Statement balance excludes billed-not-posted items",
 "The statement balance is the ledger balance less interest, service, misc, insurance and membership amounts that are billed but not yet posted.",
 "COMPUTE CM-RTL1-BALANCE-STMT = CM-RTL1-BALANCE\n  - (CM-RTL-IBNP + CM-RTL-SVC-BNP + CM-RTL-MISC-FEES\n     + CM-RTL-INSUR-BNP + CM-RTL-MEMBER-BNP + CM-RTL1-FEE)",
 "CPD110","RESET-ACCOUNT",16597,"CM-RTL-IBNP, CM-RTL-SVC-BNP",
 "BNP = billed not posted. IBNP = interest billed not posted."),

("BAL-05","Balances & statement","Cash statement balance",
 "Same treatment on the cash side.",
 "COMPUTE CM-CASH1-BALANCE-STMT = CM-CASH1-BALANCE\n  - (CM-CASH-IBNP + CM-CASH-SVC-BNP + CM-CASH1-FEE)",
 "CPD110","RESET-ACCOUNT",16630,"CM-CASH-IBNP, CM-CASH-SVC-BNP",""),

("BAL-06","Balances & statement","Statement totals",
 "Retail and cash statement balances totalled for presentation.",
 "COMPUTE WS-RTL-STMT-BAL = CM-RTL1-BALANCE-STMT\n  + CM-RTL2-BALANCE-STMT + CM-RTL3-BALANCE-STMT\nCOMPUTE WS-CASH-STMT-BAL = CM-CASH1-BALANCE-STMT + CM-CASH2-BALANCE-STMT",
 "CPD110","(statement build)",27784,"CM-*-BALANCE-STMT",""),

("BAL-07","Balances & statement","Prior month closing principal and interest",
 "At cycle close the principal (balance plus instalment balance) and the accrued interest are snapshotted.",
 "COMPUTE CM-PREV-MTH-CLOSE-PRIN = CM-CURR-BALANCE + CM-INSTL-BAL\nCOMPUTE CM-PREV-MTH-CLOSE-INTR ROUNDED =\n  CM-CASH-ACCRUED-INTR + CM-CASH2-ACCRUED-INTR (+ retail terms)",
 "CPD110","CARDHOLDER-PROCESSING",4793,"CM-INSTL-BAL",""),

# ---------------- I. Rewards ----------------
("RWD-01","Rewards & rebate","Bonus points earned in the cycle",
 "Net qualifying retail spend — debits less miscellaneous charges, less the annual fee, less non-payment credits — multiplied by the bonus rate.",
 "COMPUTE WS-BONUS-BUCKS-EARNED ROUNDED =\n  ((CM-RTL-AMNT-DB - CM-RTL-MISC-CTD) - WS-TEMP-ANN-FEE\n   - (CM-RTL-AMNT-CR - CM-RTL-PYMT-CTD)) * TCM-BONUS-PERCENT",
 "CPD110","STATEMENT-PREPARATION",14809,"TCM-BONUS-PERCENT",
 "Refunds reduce earned points; payments do not, which is why payments are added back."),

("RWD-02","Rewards & rebate","Bonus balance roll-forward",
 "Opening bonus balance plus points earned less points redeemed in the cycle.",
 "COMPUTE CM-BB-BEG-BALANCE = CM-BB-BEG-BALANCE\n  + WS-BONUS-BUCKS-EARNED - CM-BB-USED-CTD",
 "CPD110","STATEMENT-PREPARATION",15238,"CM-BB-USED-CTD",""),

("RWD-03","Rewards & rebate","Cashback amount from Visa clearing",
 "Cashback arrives in minor units and is rescaled to the destination currency's decimal convention.",
 "COMPUTE WS-AMT =\n  (CXVSA-FIN-TCR1-CASHBACK / 100) * (10 ** WS-DST-CCY-EXP)",
 "CXCV010","CCCC0-FMT-PR-RE-CB-TCR1",6448,"WS-DST-CCY-EXP",""),

("RWD-04","Rewards & rebate","Merchant rebate in the daily settlement",
 "Merchant rebate fees are added back when the merchant's carried-forward balance is struck.",
 "COMPUTE WS-TOT-AMT-MER-RB-FEE = MAR-CAC-REBATE-FEE (WS-SUB)",
 "CQD720","A000-INITIAL-PROCESSING",6294,"MAR-CAC-REBATE-FEE",""),

# ---------------- J. Tax ----------------
("TAX-01","Tax (GST / SST)","GST on merchant discount",
 "Tax is the discount amount multiplied by the GST rate held on the transaction, divided by 100.",
 "COMPUTE WT-BDE-T-ENR-GST-AMT ROUNDED =\n  CQBDTE-T-ENR-DIS-AMT * CQBDTE-T-GST-RTE / 100",
 "CQD720","C770-PROCESS-BDTE-DETAIL",3617,"CQBDTE-T-GST-RTE",
 "The rate travels on the transaction record, so a rate change applies from its effective date."),

("TAX-02","Tax (GST / SST)","Daily discount GST net of enrolment GST",
 "Total discount GST for the day less the GST already taken on enrolment fees.",
 "COMPUTE WS-DLY-DISC-GST = WS-TOT-DISC-GST\n  - WT-MCC-ENR-GST-AMT - WT-MCD-ENR-GST-AMT - WT-MPR-ENR-GST-AMT",
 "CQD720","(daily totals)",1975,"WS-TOT-DISC-GST",""),

("TAX-03","Tax (GST / SST)","Net sales grossed up by enrolment GST",
 "Enrolment GST is added back into net sales so the settlement figure reconciles.",
 "COMPUTE WS-DLY-NET-SALES = WS-TOT-NET-SALES\n  + WT-MCC-ENR-GST-AMT + WT-MCD-ENR-GST-AMT + WT-MPR-ENR-GST-AMT",
 "CQD720","(daily totals)",1980,"WS-TOT-NET-SALES",""),

("TAX-04","Tax (GST / SST)","GST sign reversal on the statement detail",
 "GST is flipped in sign when written to the merchant statement detail record.",
 "COMPUTE MSTD1-GST-AMT = WT-BDE-T-DIS-GST-AMT * -1\nCOMPUTE MSAD1-GST-AMT = CQBDTE-T-FEE-GST-AMT * -1",
 "CQD720","C770-PROCESS-BDTE-DETAIL",3716,"WT-BDE-T-DIS-GST-AMT",
 "Fees are debits to the merchant, hence the sign flip for presentation."),

("TAX-05","Tax (GST / SST)","Interest expense to the YTD tax buckets",
 "Interest paid is accumulated into calendar and fiscal year-to-date buckets for tax reporting.",
 "ADD CMT-AMNT TO CM-IE-YTD CM-IE-TAX-YTD\n  OC-INTEREST-PAID-CALENDAR-YTD OC-INTEREST-PAID-FISCAL-YTD",
 "CPD110","TRANSACTION-PROCESSING",11519,"CM-IE-TAX-YTD",""),

# ---------------- K. Merchant discount ----------------
("MDR-01","Merchant discount (MDR)","Average discount rate across cards",
 "Total discount divided by the card count gives the average rate for the merchant.",
 "COMPUTE WS-AVG-DISC-RATE = WS-TOT-DISC / WS-CARD-COUNT",
 "CPM320","6005-COMPUTE-FEE-BASED-SALES",10152,"WS-TOT-DISC, WS-CARD-COUNT",
 "Guard: only reached when WS-CARD-COUNT is non-zero."),

("MDR-02","Merchant discount (MDR)","Effective rate after volume concession",
 "The average rate is reduced by a concession looked up on discount type, sales band and range.",
 "COMPUTE WS-DISC-RATE = WS-AVG-DISC-RATE\n  - OCMDM-PCT-UNDER-BASE-RATE (X-OCM-DISC, X-OCM-SALES, X-OCM-RANGE)",
 "CPM320","6030-COMPUTE-RATE",10359,"OCMDM-PCT-UNDER-BASE-RATE",
 "Three-dimensional table: higher volume earns a bigger reduction."),

("MDR-03","Merchant discount (MDR)","Discount amount charged to the merchant",
 "Fee-based sales multiplied by the effective discount rate.",
 "COMPUTE MMD-AMT-DISC (1) ROUNDED =\n  WS-AMT-FEE-BASED-SALES * WS-DISC-RATE",
 "CPM320","6030-COMPUTE-RATE",10375,"WS-AMT-FEE-BASED-SALES, WS-DISC-RATE",""),

("MDR-04","Merchant discount (MDR)","Discount accumulated across sales bands",
 "Each sales band's amount is rated separately and added to the running discount.",
 "COMPUTE MMD-AMT-DISC (1) ROUNDED =\n  MMD-AMT-DISC (1) + (WS-FBS-AMNT * WS-DISC-RATE)",
 "CPM320","6045-CRBD-SALES-RANGES",10430,"WS-FBS-AMNT",""),

("MDR-05","Merchant discount (MDR)","Back-solve the effective rate",
 "The blended rate actually charged, derived from the discount taken over the sales it was taken on.",
 "COMPUTE WS-DISC-RATE = MMD-AMT-DISC (1) / WS-AMT-FEE-BASED-SALES",
 "CPM320","6040-COMPUTE-RATE-BAND-DISC",10397,"MMD-AMT-DISC",
 "Used for the rate shown on the merchant statement."),

("MDR-06","Merchant discount (MDR)","Merchant settlement (ACH) amount",
 "Sales less returns across all card schemes gives the amount to pay the merchant.",
 "COMPUTE WS-SALES =\n  MMD-VI-AMT-TOTAL-SALES (1) - MMD-VI-AMT-TOTAL-RETURNS (1)\n  + MMD-MC-... + MMD-JCB-... (per scheme)\nCOMPUTE CPWMMR-MK4-ACH-AMOUNT = WS-SALES * -1",
 "CPM320","5710-GEN-ACH-MERCH-DEPOSIT",10005,"MMD-*-AMT-TOTAL-SALES/RETURNS",
 "Sign is flipped for the outgoing payment instruction."),

("MDR-07","Merchant discount (MDR)","Discount and fees withheld from settlement",
 "Discount plus fees are settled as a separate ACH debit.",
 "COMPUTE CPWMMR-MK4-ACH-AMOUNT = (MMD-AMT-DISC (2) + MMD-AMT-FEES (2))",
 "CPM320","5730-GENERATE-ACH-DISCOUNT",10111,"MMD-AMT-DISC, MMD-AMT-FEES",""),

("MDR-08","Merchant discount (MDR)","Merchant balance carried forward",
 "Opening balance plus net sales and payment adjustments, less adjustments, fees and fee GST, plus rebates.",
 "COMPUTE MAR-BALANCE-CF = MAR-BALANCE-BF + WS-TOT-NET-SALES\n  + WS-TOT-PAYMENT-ADJ - WS-TOT-ADJUSTMENT - WS-TOT-FEES\n  - WS-TOT-FEES-GST + WS-TOT-AMT-MER-RB-FEE + WS-AMT-REBATE",
 "CQD720","A000-INITIAL-PROCESSING",2009,"MAR-BALANCE-BF",
 "The merchant accounting equivalent of a statement roll-forward."),

# ---------------- L. Interchange ----------------
("ICG-01","Interchange","Net item interchange fee",
 "A per-item fee times the item count, plus an ad-valorem rate times the amount — both looked up by acquirer region, issuer region and programme.",
 "COMPUTE WS-MC-NFI-FEE (lvl) =\n  (WS-MC-NFI-NBR (lvl) * WS-ICG-RTL-PGM-ITEM (acq, iss, pgm))\n  + (WS-MC-NFI-AMT (lvl) * WS-ICG-RTL-PGM-RATE (acq, iss, pgm))",
 "CPD030","CALC-MC-BATCH-NET-ITEM-FEE",5806,"WS-ICG-RTL-PGM-ITEM, WS-ICG-RTL-PGM-RATE",
 "The standard scheme interchange shape: fixed per transaction plus a percentage."),

("ICG-02","Interchange","Interchange fee sign",
 "The interchange figure is negated to express it as a cost.",
 "COMPUTE WS-MC-BATCH-INTCHG-FEE ROUNDED = WS-MC-SI-AMT3 * -1.00",
 "CPD030","CALC-MC-BATCH-NET-ITEM-FEE",5827,"WS-MC-SI-AMT3",""),

("ICG-03","Interchange","Batch net amount",
 "Cash advance and ATM amounts are folded into the batch net.",
 "COMPUTE WS-MC-BATCH-NET-AMT = WS-MC-BATCH-NET-AMT\n  + WS-MC-BATCH-AMT-CASH-ADV + WS-MC-BATCH-AMT-ATM",
 "CPD030","CALC-MC-BATCH-NET-ITEM-FEE",5831,"WS-MC-BATCH-AMT-CASH-ADV",""),

("ICG-04","Interchange","Batch gross including fees",
 "Net plus interchange, cash advance and ATM fees gives the settlement figure for the batch.",
 "COMPUTE WS-MC-BATCH-AMT = WS-MC-BATCH-NET-AMT\n  + WS-MC-BATCH-INTCHG-FEE + WS-MC-BATCH-FEE-CASH-ADV\n  + WS-MC-BATCH-FEE-ATM",
 "CPD030","CALC-MC-BATCH-NET-ITEM-FEE",5835,"WS-MC-BATCH-INTCHG-FEE",""),

("ICG-05","Interchange","Visa interchange rate maintenance",
 "Scheme interchange rates are held on the organisation control record and maintained by percentage or absolute change.",
 "COMPUTE FM1-NO-47-VISA-INTCHG-RATE (i) =\n  OCM-VISA-INTCHG-RATE (j) * WS-PERCENT-HOLD\n  (or + / - WSCPS-MAINT-FIELD-NUMERIC)",
 "CPU600","4450-FILL-FM-47",4695,"OCM-VISA-INTCHG-RATE",
 "CPU600 is the mass-maintenance program; it changes the rates the batch then applies."),

# ---------------- M. Currency ----------------
("FX-01","Currency conversion","Minor-unit rescaling on Visa clearing",
 "Visa carries amounts in minor units with a currency exponent; the amount is divided by 100 and rescaled by 10 to the power of that exponent.",
 "COMPUTE WS-AMT =\n  (CXVSA-DSP-TCR1-DEST-AMT / 100) * (10 ** WS-DST-CCY-EXP)",
 "CXCV010","CCKC0-FMT-TC33-RE-CB-TCR1",10188,"WS-DST-CCY-EXP",
 "Handles currencies with 0, 2 or 3 decimal places from one wire format."),

("FX-02","Currency conversion","Visa conversion rate is read, not computed",
 "The Visa rate is read once from the VISRATE file at the start of the run and held for the whole job. "
 "An empty file is fatal — the program abends rather than convert at a wrong rate.",
 "OBTAIN-VISA-CURRENCY-RATE.\n  OPEN INPUT VMC-CURRENCY-RATE-FILE\n  READ VMC-CURRENCY-RATE-FILE\n    AT END MOVE 88888 TO WS-ABEND-CODE\n           MOVE 'VISRATE FILE IS EMPTY' TO WS-ABENDMSG\n           PERFORM ZZZZ-ABEND\n  MOVE VMC-VISA-RATE TO WS-VISA-RATE\n  CLOSE VMC-CURRENCY-RATE-FILE",
 "CSM08","OBTAIN-VISA-CURRENCY-RATE",2142,"VMC-VISA-RATE, VMC-SCALE-FACTOR",
 "Rate maintenance is a data change, not a code change. NOTE: the older CPRTB currency-rate-table "
 "path (WS-IN-ORG-RATE = CPRTB-INCOM-RATE / 10**exponent, and cash fee rate = rate * 0.99) is "
 "commented out in CALC-CURR-CONV-RATE and in CPD030 - do not mistake it for live logic."),

# ---------------- N. Instalment ----------------
("INS-01","Instalment / fixed-term loan","Months on which interest is payable",
 "Repayment term less the interest-free period.",
 "COMPUTE WS-FTL-MNTHS-INT-PAYABLE =\n  (CMA-FTL-REPAYMENT-TERM - CMA-FTL-INT-FREE-PERIOD)",
 "CPD110","(fixed-term loan build)",27507,"CMA-FTL-REPAYMENT-TERM, CMA-FTL-INT-FREE-PERIOD",""),

("INS-02","Instalment / fixed-term loan","Insurance premium share of the instalment",
 "The premium's share of the instalment due, pro-rated by premium over premium plus principal.",
 "COMPUTE WS-AMNT4 = ((WS-FTL-TOT-DUE-TD - WS-FTL-TOT-INT-TD)\n  * (CMA-FTL-INS-PREMIUM\n     / (CMA-FTL-INS-PREMIUM + WS-FTL-TOT-PRNCPL-AMNT)))",
 "CPD110","(fixed-term loan build)",27936,"CMA-FTL-INS-PREMIUM",""),

("INS-03","Instalment / fixed-term loan","Total loan principal",
 "The four principal tranches added together.",
 "COMPUTE CRR-R45-PRINCIPAL-AMT = (CMA-FTL-LOAN-PRNCPL1\n  + CMA-FTL-LOAN-PRNCPL2 + CMA-FTL-LOAN-PRNCPL3 + CMA-FTL-LOAN-PRNCPL4)",
 "CPD110","REPORTS-AND-TRANSACTIONS",17059,"CMA-FTL-LOAN-PRNCPL1..4",""),

("INS-04","Instalment / fixed-term loan","Instalment exposure for authorisation",
 "Instalment balance plus outstanding instalment authorisations.",
 "COMPUTE ACR-INSTL-BAL = CM-INSTL-BAL + CM-AMNT-OUTST-INSTL",
 "CPD110","9400-CUSTOMER-CALCULATE",29111,"CM-INSTL-BAL",""),

("INS-05","Instalment / fixed-term loan","Credit used including instalment share",
 "Credit used is increased by the configured share of the instalment balance.",
 "COMPUTE ACR-CREDIT-USED = ACR-CREDIT-USED\n  + (TC-INSTL-EM-AVL-PER * CM-INSTL-BAL)",
 "CPD110","9400-CUSTOMER-CALCULATE",29114,"TC-INSTL-EM-AVL-PER",""),

# ---------------- O. Provision / charge-off ----------------
("GL-01","Provision & charge-off","Provisional interest net",
 "Provisional interest less negative provisional interest, accumulated for the general ledger.",
 "COMPUTE WST-PROVISIONAL ROUNDED = WST-PROVISIONAL\n  + CM-RTL-PROVIS-INTR - CM-RTL-NEG-PROVIS-INTR",
 "CPD110","CARDHOLDER-PROCESSING",7038,"CM-RTL-PROVIS-INTR",
 "CPD110B1 carries the same computation over the ABP (account balance process) record."),

("GL-02","Provision & charge-off","Interest on the provisional balance",
 "Daily fraction times the provisional retail balance times the rate.",
 "COMPUTE WSP-INT ROUNDED =\n  WSI-DAY-FACTOR * WSP-RTL-PROVIS-BAL * WSI-RATE-1",
 "CPD110","9500-SORT-SUSPENSE-SORT-FILE",29466,"WSP-RTL-PROVIS-BAL",
 "Suspended interest on delinquent accounts: accrued but not taken to income."),

("GL-03","Provision & charge-off","Gross charge-off",
 "Bad-debt, bankruptcy, fraud and counterfeit write-offs added into one gross charge-off figure.",
 "COMPUTE WSS117-CQ-AX3F-GROSS-CHGOFF (n) =\n  ...BDEBT-WTEOFF + ...BKRUPT-WTEOFF\n  + ...FRAUD-LOSSES + ...CTFEIT-LOSSES + ...",
 "CPU515","PRINT-SCHEDULE-TYPE",7035,"WSS117-CQ-AX-* buckets",
 "Feeds the quarterly affiliation / regulatory schedule."),

("GL-04","Provision & charge-off","Interest activity to the general ledger",
 "Each accrual is mirrored to a GL amount and posted through the cardholder GL routine.",
 "COMPUTE WS-AMOUNT-GL ROUNDED = WSI-ACCRUAL\n  PERFORM GENERATE-INT-ACTIV-GL / GGTG-UPD-CARDH-GL",
 "CPD110","INTEREST-PROCESSING",12502,"WS-AMOUNT-GL",
 "Keeps the subsidiary ledger and the GL in step day by day."),

("GL-05","Provision & charge-off","Rounding to the cent on GL transactions",
 "Half a cent is added before the amount is moved to the transaction field, giving round-half-up.",
 "COMPUTE GT-AMNT = WSI-ACCRUAL + .005",
 "CPD110","REPORTS-AND-TRANSACTIONS",17669,"WSI-ACCRUAL",
 "The receiving field has two decimals, so the MOVE truncates the rest."),
]

# Parameters / rate drivers
PARAMETERS = [
 ("TCM-CASH-LIMIT-PERCENT","Product (TCM) table","Share of the credit limit available as cash","Fraction","LMT-01","CPD110"),
 ("TCM-INSTL-LIMIT-PERCENT","Product (TCM) table","Share of the credit limit available for instalments","Fraction","LMT-02","CPD110"),
 ("TCM-OVER-LIMIT","Product (TCM) table","Multiplier giving the permitted over-limit tolerance","Multiplier (e.g. 1.10)","LMT-03, LMT-04","CPD110"),
 ("TCM-LATE-CHARGE","Product (TCM) table","Flat late charge","Amount","LATE-03, LATE-04, LATE-05","CPD110"),
 ("TCM-LC-PERCENT","Product (TCM) table","Late charge as a percentage of unpaid balance","Fraction","LATE-03, LATE-05","CPD110"),
 ("TCF-LATE-CHARGE-FLAG","Product control","Selects which late-charge formula applies (0/5 flat, 2 flat+percent)","Code","LATE-03, LATE-04","CPD110"),
 ("TCM-MINIMUM-PYMT","Product (TCM) table","Floor under the computed minimum payment","Amount","MIN-10","CPD110"),
 ("TCM-PYMT-THRESHOLD","Product (TCM) table","Balance below which the minimum floor is not applied","Amount","MIN-10","CPD110"),
 ("TCM-PAYMENT-TERM","Product (TCM) table","Divisor or percentage used on the revolving balance","Number","MIN-06, MIN-07, MIN-09","CPD110"),
 ("TCM-DERIVE-METHOD","Product (TCM) table","0 = divide by term, non-zero = multiply by term as a percentage","Code","MIN-06, MIN-07","CPD110"),
 ("TCP-PERCENT (ITCP)","Fixed-payment table","Percentage of principal used to set the fixed payment","Fraction","MIN-03","CPD110"),
 ("TCM-BONUS-PERCENT","Product (TCM) table","Bonus points earned per unit of net qualifying spend","Fraction","RWD-01","CPD110"),
 ("TC-CA-PER-SRCE (ICAP)","Cash advance fee table","Transaction source code the fee row applies to","Code","CAF-01","CPD110"),
 ("TC-CA-PER-LIMIT (ICAP)","Cash advance fee table","Band limit splitting rate 1 from rate 2","Amount","CAF-03, CAF-04","CPD110"),
 ("TC-CA-PER-RATE-1 (ICAP)","Cash advance fee table","First-band cash advance fee rate","Percent (/100 in code)","CAF-02, CAF-03, CAF-04","CPD110"),
 ("TC-CA-PER-RATE-2 (ICAP)","Cash advance fee table","Rate applied above the band limit","Percent (/100 in code)","CAF-04","CPD110"),
 ("TC-CA-PERCENT-MIN-CHRG","Cash advance fee table","Minimum cash advance fee","Amount","CAF-05","CPD110"),
 ("TC-CA-PERCENT-MAX-CHRG","Cash advance fee table","Maximum cash advance fee","Amount","CAF-05","CPD110"),
 ("TCSC-LIMIT (ISC)","Service charge table","Free / first-band transaction count","Count","SVC-01","CPD110"),
 ("TCSC-RATE-1 (ISC)","Service charge table","Charge per transaction in the first band","Amount","SVC-01, SVC-02","CPD110"),
 ("TCSC-RATE-2 (ISC)","Service charge table","Charge per transaction above the band","Amount","SVC-01","CPD110"),
 ("TCSC-MAXIMUM","Service charge table","Cap on total service charges","Amount","SVC-04","CPD110"),
 ("TSC-RETAIL (ISC)","Service charge table","Whether the charge posts to retail or cash","Flag","SVC-03","CPD110"),
 ("CM-CI-RATE-1/2/3","Cardholder master","Cash interest rate per band","Fraction","INT-03..INT-06, INT-13","CPD110"),
 ("CM-CI-ADJ-1/2/3","Cardholder master","Account-level adjustment to the cash rate","Fraction","INT-13","CPD110"),
 ("CM-RI-RATE-1/2/3","Cardholder master","Retail interest rate per band","Fraction","INT-03..INT-06","CPD110"),
 ("CM-RI-ADJ-1/2/3","Cardholder master","Account-level adjustment to the retail rate","Fraction","INT-13","CPD110"),
 ("WSI-LIMIT-1 / WSI-LIMIT-2","Working (from rate table)","Band boundaries for tiered interest","Amount","INT-04, INT-05","CPD110"),
 ("YEAR-BASE-360 / 365 / 366","Product control","Day-count basis for interest","Flag","INT-01","CPD110"),
 ("TCICB-RATE-1 / TCICB-RATE-2","Credit balance interest table","Rate paid on credit balances, by band","Fraction","INT-16","CPD110"),
 ("TCICB-LIMIT-2 / TCICB-LIMIT-3","Credit balance interest table","Band boundary, and cap on the credit balance that earns interest","Amount","INT-16","CPD110"),
 ("FREEZE-INTEREST (IBC)","Bank control","Suppresses all interest accrual","Flag","INT-12","CPD110"),
 ("CASH-INTR-FREE / RETAIL-INTR-FREE","Cardholder master","Grace / interest-free status per bucket","Flag","INT-11","CPD110"),
 ("TC-WAIVE-LATE-CHRG (IBC)","Bank control","Waives late charges","Flag","LATE-02","CPD110"),
 ("TC-INSTL-EM-AVL-PER","Product control","Share of instalment balance reserved from available credit","Fraction","LMT-06, INS-05","CPD110"),
 ("CQBDTE-T-GST-RTE","Merchant transaction record","GST rate carried on the transaction","Percent (/100 in code)","TAX-01","CQD720"),
 ("OCMDM-PCT-UNDER-BASE-RATE","Organisation merchant table","Volume concession off the base discount rate","Fraction","MDR-02","CPM320"),
 ("OCM-VISA-INTCHG-RATE","Organisation control","Visa interchange rate held for maintenance","Fraction","ICG-05","CPU600"),
 ("WS-ICG-RTL-PGM-ITEM / -RATE","Interchange table","Per-item fee and ad-valorem rate by region and programme","Amount / fraction","ICG-01","CPD030"),
 ("WS-DST-CCY-EXP","Currency table","Destination currency decimal exponent","Exponent","FX-01, RWD-03","CXCV010"),
 ("CMA-FTL-REPAYMENT-TERM","Fixed-term loan record","Loan repayment term in months","Months","INS-01","CPD110"),
 ("CMA-FTL-INT-FREE-PERIOD","Fixed-term loan record","Interest-free months at the start of the loan","Months","INS-01","CPD110"),
 ("CMA-FTL-INS-PREMIUM","Fixed-term loan record","Insurance premium financed with the loan","Amount","INS-02","CPD110"),
]

# Program roles
PROGRAMS = [
 ("CPD110","Batch","Cardholder daily / cycle engine — interest accrual, fees, statement preparation, minimum payment. The single most important financial program in Cardlink MY."),
 ("CPD110B1","Batch","Account balance process (ABP) extension of CPD110 — provisional interest and balance record rebuild."),
 ("CPD110NT","Batch","CPD110 note / transaction-code handling variant."),
 ("CPD130","Batch","Cardholder file maintenance and downstream balance processing."),
 ("CPD030","Batch","Scheme clearing and merchant deposit processing — MasterCard interchange and batch settlement."),
 ("CPD813","Batch","Merges CPD110 updates into the CPQAF file."),
 ("CPM320","Batch","Merchant discount (MDR), merchant ACH settlement and merchant statement information."),
 ("CPM323","Batch","Updates merchant transaction volume totals."),
 ("CPM326","Batch","Merchant fees and settlement general-ledger interface."),
 ("CPM340","Batch","Merchant report print program."),
 ("CPM370","Batch","Merchant management report."),
 ("CPM371","Batch","Merchant management reporting extension."),
 ("CPS864B","Batch","Cardholder / system reporting series."),
 ("CPU501","Batch","Quarterly affiliation report print program."),
 ("CPU515","Batch","Quarterly schedules — charge-off, write-off and loss reporting."),
 ("CPU600","Batch","Mass maintenance — applies rate and limit changes to control records."),
 ("CQD720","Batch","Merchant accounting — daily discount, GST and merchant balance roll-forward."),
 ("CXCV010","Batch","Visa incoming clearing file processing — amounts, currency exponents, cashback."),
 ("CXRC020","Batch","Scheme reconciliation processing."),
 ("QMR123","Batch","Acquirer module batch reporting."),
]

# --- second tranche (22 additional programs) -------------------------------
from catalogue_add import CATALOGUE_2, PROGRAMS_2, PARAMETERS_2
CATALOGUE  = CATALOGUE  + CATALOGUE_2
PROGRAMS   = sorted(PROGRAMS + PROGRAMS_2)
PARAMETERS = PARAMETERS + PARAMETERS_2

# --- third tranche (16 further programs) -----------------------------------
from catalogue_add2 import CATALOGUE_3, PROGRAMS_3, PARAMETERS_3
CATALOGUE  = CATALOGUE  + CATALOGUE_3
PROGRAMS   = sorted(PROGRAMS + PROGRAMS_3)
PARAMETERS = PARAMETERS + PARAMETERS_3

# --- fourth tranche (CCOM, monthly interest, scheme gaps) -------------------
from catalogue_add3 import CATALOGUE_4, PROGRAMS_4, PARAMETERS_4
CATALOGUE  = CATALOGUE  + CATALOGUE_4
PROGRAMS   = sorted(PROGRAMS + PROGRAMS_4)
PARAMETERS = PARAMETERS + PARAMETERS_4

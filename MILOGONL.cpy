      *---------------------------------------------------------------*
      * MILOGONL - ONLINE MILOG1/2/3 VSAM (IAM) LOG RECORD LAYOUT     *
      * WITH FULL PER-TRANSACTION MAPS FOR THE MY SYSTEM              *
      *   MY: xxxMBI.ONLVSM.MYnnnn.MILOGn  KEYS(42,0) REC(252,8047)   *
      *   SG: xxxMBI.ONLVSM.SGnnnn.MILOGn  KEYS(42,0) REC(252,8349)   *
      *---------------------------------------------------------------*
      * SOURCE: MIC004 (ACTIVITY LOG RECORD), MIC003 (QUEUE FILE ISO/ *
      * 8583 RECORD, FULL BODY INCL ALL 52 PER-TXN DE48 REDEFINES),   *
      * MIC002 RESPONSE PAYLOADS, IDCAMS DEFINE MIDFLOG2, MISBIZ FD.  *
      *                                                               *
      * DO NOT USE MILOGDAT / MILOGMAP ON THESE FILES - THOSE MAP THE *
      * FIXED-8000 DAILY BATCH EXTRACT (CLKMLOG.DAT).  THE ONLINE     *
      * RECORD IS VARIABLE LENGTH WITH COMP-3 PACKED KEY/AMOUNTS.     *
      *                                                               *
      * RECORD TYPES (MIC004-REC-TYPE):                               *
      *   A/B ACTIVITY LOG (MESSAGE)   - DATA AREA = MIC003 RECORD    *
      *   M   SYSTEM CONTROL MAINT LOG - DATA AREA = MAINT IMAGE      *
      *   N/O CIA NON-MONETARY MAINT   - DATA AREA = 84-BYTE DATA     *
      *   X   SYSTEM MESSAGES LOG      - DATA AREA = MESSAGE TEXT     *
      *   S   SMS LOG VIA CMBI (MY)                                   *
      * REC-STATUS: " " NORMAL, R REVERSED, D DECLINED, U UNMATCHED   *
      * REVERSAL, M MATCHED REVERSAL, P PRPP DUPLICATE (MY).          *
      *                                                               *
      * ABSOLUTE BYTE MAP - MY RECORD (1-BASED):                      *
      *   KEY 1-42 (DATE/TIME/TRACE/SEQ COMP-3), HEADER 43-168,       *
      *   MIC003 DATA AREA 169-8047:                                  *
      *     IDENTIFIER 169-267, MSG-TYPE 268-271, BITMAP 272-399,     *
      *     ISO FIXED DES 400-2041 -                                  *
      *       DE48 ADDTL DATA 865-1863 (TRANS-CODE 865-868, COMMON    *
      *       PREFIX 865-1014, PER-TXN MIC003-B048-xxxx-DATA          *
      *       REDEFINES AT 1015-1863),                                *
      *     OUTPUT SLOTS: B060 2044-3042, B061 3045-4043,             *
      *       B062 4046-5044, B063 5047-6045, B116 6048-7046,         *
      *       B117 7049-8047.                                         *
      * PER-TXN RESPONSE MAPS ML60-<TXN> (MIC002 PAYLOADS) REDEFINE   *
      * MIC003-B060-OUTPUT-DATA-1; PAYLOADS THAT SPILL INTO B061-B117 *
      * REPEAT THE SAME LAYOUT AT +1001 BYTES PER SLOT.               *
      * MAINT/UPDATE TXNS HAVE NO OUTPUT PAYLOAD - RESULT IS DE39     *
      * (MIC003-B039-ACTION-CODE) ONLY.                               *
      *---------------------------------------------------------------*
      * LAYOUT 1 - MALAYSIA (MAX LRECL 8047) - FULL DETAIL            *
      *---------------------------------------------------------------*
       01  MILOG-ONL-RECORD-MY.
           03  MIC004-LOG-FILE-KEY.
               05  MIC004-CARDHOLDER-NMBR        PIC X(19).
               05  MIC004-ALT-KEY.
                   07  MIC004-TRANSACTION-DATE   PIC S9(08)
                                                 COMP-3.
                   07  MIC004-TRANSACTION-TIME   PIC S9(06)
                                                 COMP-3.
                   07  MIC004-DELIVERY-CHANNEL   PIC X(08).
                   07  MIC004-TRACE-NUMBER       PIC S9(06)
                                                 COMP-3.
                   07  MIC004-SEQUENCE-NUMBER    PIC S9(03)
                                                 COMP-3.
           03  MIC004-MTI                        PIC S9(04)
                                                 COMP-3.
           03  MIC004-REC-TYPE                   PIC X(01).
           03  MIC004-DATE-STAMP                 PIC S9(08)
                                                 COMP-3.
           03  MIC004-TIME-STAMP                 PIC S9(06)
                                                 COMP-3.
           03  MIC004-REC-STATUS                 PIC X(01).
           03  MIC004-NETWK-POS-DATA-CODE        PIC X(12).
           03  MIC004-CARD-TYPE                  PIC X(01).
               88  MIC004-PRIVATE-LABEL          VALUE 'P'.
               88  MIC004-VISA-CARD              VALUE 'V'.
               88  MIC004-MSTR-CARD              VALUE 'M'.
               88  MIC004-JCB-CARD               VALUE 'J'.
               88  MIC004-AMEX-CARD              VALUE 'X'.
               88  MIC004-DB-CARD                VALUE 'D' 'E'.
           03  MIC004-TXN-IC                     PIC X(02).
           03  FILLER                            PIC X(97).
           03  MIC004-DATA-AREA                  PIC X(7879).
      *
      * ---- TYPE A/B RECORDS: DATA AREA = MIC003 QUEUE RECORD ----
      * (COPYBOOK MIC003 VERBATIM, LEVEL NUMBERS +2)
           03  MIC004-MIC003-REC REDEFINES MIC004-DATA-AREA.
               05  MIC003-QUEUE-IDENTIFIER-FIELDS.
                   07  MIC003-DATE-RECEIVED PIC 9(08).
                   07  MIC003-TIME-RECEIVED PIC 9(06).
                   07  MIC003-TERMINAL-ID PIC X(04).
                   07  MIC003-TRACE-IND PIC X(01).
                   07  MIC003-SAVE-AREA PIC X(50).
                   07  MIC003-CARD-TYPE PIC X(01).
                       88  MIC003-PRIVATE-LABEL VALUE 'P'.
                       88  MIC003-VISA-CARD VALUE 'V'.
                       88  MIC003-MSTR-CARD VALUE 'M'.
                       88  MIC003-JCB-CARD VALUE 'J'.
                       88  MIC003-AMEX-CARD VALUE 'X'.
                       88  MIC003-DB-CARD VALUE 'D'.
                       88  MIC003-VDB-CARD VALUE 'E'.
                   07  MIC003-IPM-DE22-POS-DATA-CODE PIC X(12).
                   07  MIC003-VISA-DE22 REDEFINES
                           MIC003-IPM-DE22-POS-DATA-CODE.
                     09  MIC003-POS-ENTRY-MODE-V PIC X(02).
                     09  FILLER PIC X(10).
                   07  MIC003-TXN-IC PIC X(02).
                   07  MIC003-ROUTE-DEST-IND PIC X(01).
                   07  MIC003-TCP-QUEUE PIC X(08).
                   07  FILLER PIC X(06).
               05  MIC003-QUEUE-MESSAGE-RECORD.
                   07  MIC003-MESSAGE-TYPE-ID PIC 9(04).
                   07  MIC003-BYTE-MAP-IND-REC PIC X(128).
                   07  FILLER REDEFINES MIC003-BYTE-MAP-IND-REC.
                     09  MIC003-BYTE-MAP-IND OCCURS 128 TIMES INDEXED
                             BY X-MIC003-BMI PIC X(01).
                   07  MIC003-QUEUE-REC PIC X(7648).
                   07  FILLER REDEFINES MIC003-QUEUE-REC.
                     09  MIC003-FIX-LENGTH-QUEUE-REC.
                       11  MIC003-B002-PAN-LEN PIC S9(02) COMP-3.
                       11  MIC003-B002-PAN-19 PIC X(19).
                       11  FILLER REDEFINES MIC003-B002-PAN-19.
                         13  MIC003-B002-PAN-18 PIC 9(18).
                         13  FILLER PIC X(01).
                       11  FILLER REDEFINES MIC003-B002-PAN-19.
                         13  MIC003-B002-PAN-17 PIC 9(17).
                         13  FILLER PIC X(02).
                       11  FILLER REDEFINES MIC003-B002-PAN-19.
                         13  MIC003-B002-PAN-16 PIC 9(16).
                         13  FILLER PIC X(03).
                       11  FILLER REDEFINES MIC003-B002-PAN-19.
                         13  MIC003-B002-PAN-15 PIC 9(15).
                         13  FILLER PIC X(04).
                       11  MIC003-B003-PROCESSING-CODE PIC 9(06).
                           88  LOCAL-CHEQUE VALUE 600010.
                           88  RETURN-LOCAL-CHEQUE VALUE 600030.
                           88  HOUSE-CHEQUE VALUE 600020.
                           88  CREDIT-ADVICE VALUE 600040.
                           88  PAYNET-PYMT-INQ VALUE 499999.
                       11  MIC003-B003-PROCESSING-CODE-06 REDEFINES
                               MIC003-B003-PROCESSING-CODE.
                         13  MIC003-B003-PROCESSING-CODE-02 PIC 9(02).
                             88  RETAIL-DEBIT VALUE 00.
                             88  CASH-ADVANCE VALUE 01.
                             88  BONUS-REDEMPTION VALUE 17.
                             88  PAYMENT VALUE 40.
                             88  CASH-PAYMENT VALUE 50.
                             88  CHEQUE-PAYMENT VALUE 60.
                         13  MIC003-B003-PROCESSING-CODE-04 PIC 9(04).
                       11  MIC003-B004-TRANS-AMOUNT PIC S9(10)V99
                               COMP-3.
                       11  MIC003-B011-SYS-AUDT-TRACE PIC S9(07) COMP-3.
                       11  MIC003-B012-LCL-DATE-TIME PIC S9(12) COMP-3.
                       11  MIC003-B013-DATE-EFFECTIVE PIC 9(04).
                       11  MIC003-B014-DATE-EXPIRATION PIC 9(04).
                       11  MIC003-B017-DATE-CAPTURE PIC 9(04).
                       11  MIC003-B022-POS-DATA-CODE PIC X(12).
                       11  MIC003-B024-FUNCTION-CODE PIC 9(03).
                           88  AUTHORIZATION VALUE 100.
                           88  FINANCIAL-REQUEST VALUE 200.
                           88  FILE-UPDATE VALUE 302.
                           88  INQUIRY VALUE 305.
                           88  FULL-REVERSAL VALUE 400.
                       11  MIC003-B026-CARD-ACPTOR-BIZ-CD PIC 9(04).
                       11  MIC003-B030-AMOUNT-ORIGINAL.
                         13  MIC003-B030-AMOUNT-ORIG-TRANS PIC 9(10)V99.
                         13  MIC003-B030-AMOUNT-ORIG-RECON PIC 9(10)V99.
                       11  MIC003-B035-TRACK-2-DATA-LEN PIC S9(02)
                               COMP-3.
                       11  MIC003-B035-TRACK-2-DATA PIC X(37).
                       11  MIC003-B037-RETRIEVAL-REF-NO PIC X(12).
                       11  MIC003-B038-APPROVAL-CODE PIC X(06).
                       11  MIC003-B039-ACTION-CODE PIC 9(03).
                           88  PARTIAL-SALE-TXN VALUE 002.
                           88  SUCCESFUL VALUE 300.
                           88  REC-LOCATE-FAILED VALUE 302.
                           88  FIELD-EDIT-ERROR VALUE 304.
                           88  FILE-CLOSED VALUE 305.
                           88  NOT-SUCCESSFUL VALUE 306.
                           88  ACCT-NOT-FOUND VALUE 310.
                           88  INVALID-TRANSACTION VALUE 902.
                       11  MIC003-B041-CARD-ACPTOR-TERM PIC X(08).
                       11  MIC003-B042-CARD-ACPTOR-IDEN PIC X(15).
                       11  MIC003-B043-CACPTOR-NLOC-LEN PIC S9(02)
                               COMP-3.
                       11  MIC003-B043-CARD-ACPTOR-NLOC PIC X(99).
                       11  MIC003-B044-ADDITION-RESP-LEN PIC S9(02)
                               COMP-3.
                       11  MIC003-B044-ADDITIONAL-RESP PIC X(99).
                       11  FILLER REDEFINES MIC003-B044-ADDITIONAL-RESP.
                         13  MIC003-B044-END-OF-DATA-BDS PIC X(01).
                         13  MIC003-B044-NEXT-REC-KEY-BDS PIC X(44).
                         13  FILLER REDEFINES
                                 MIC003-B044-NEXT-REC-KEY-BDS.
                             17  MIC003-B044-PLT-ORG-BDS PIC 9(03).
                             17  MIC003-B044-PLT-TYPE-BDS PIC 9(03).
                             17  MIC003-B044-PLT-NBR-BDS PIC X(19).
                             17  MIC003-B044-CUST-ORG-BDS PIC 9(03).
                             17  MIC003-B044-CUST-NBR-BDS PIC 9(16).
                         13  FILLER PIC X(54).
                       11  FILLER REDEFINES MIC003-B044-ADDITIONAL-RESP.
                         13  MIC003-B044-END-OF-DATA-IND PIC X(01).
                         13  MIC003-B044-NEXT-REC-KEY PIC X(30).
                         13  MIC003-B044-NEXT-REC-KEY-VMI1 REDEFINES
                                 MIC003-B044-NEXT-REC-KEY.
                             17  MIC003-B044-CARD-NUM-VMI1 PIC X(19).
                             17  MIC003-B044-INSTL-PL-VMI1 PIC 9(03).
                             17  MIC003-B044-IDX-VMI1 PIC 9(03).
                             17  FILLER PIC X(05).
                         13  MIC003-B044-NEXT-REC-KEY-VCIF REDEFINES
                                 MIC003-B044-NEXT-REC-KEY.
                             17  MIC003-B044-A-C-IND-VCIF PIC X(01).
                             17  MIC003-B044-VCIF-DETAIL PIC X(24).
                             17  MIC003-B044-VCIF-ACT REDEFINES
                                     MIC003-B044-VCIF-DETAIL.
                               22  MIC003-B044-A-ORG PIC 9(03).
                               22  MIC003-B044-A-TYP PIC 9(03).
                               22  MIC003-B044-A-ACT PIC 9(16).
                               22  FILLER PIC X(02).
                             17  MIC003-B044-VCIF-PLT REDEFINES
                                     MIC003-B044-VCIF-DETAIL.
                               22  MIC003-B044-CRD PIC X(19).
                               22  FILLER PIC X(05).
                             17  FILLER PIC X(05).
                         13  MIC003-B044-NEXT-REC-KEY-CCIK REDEFINES
                                 MIC003-B044-NEXT-REC-KEY.
                             17  MIC003-B044-PLASTIC-ORG PIC 9(03).
                             17  MIC003-B044-PLASTIC-TYPE PIC 9(03).
                             17  MIC003-B044-PLASTIC-NBR PIC X(19).
                             17  MIC003-B044-CUSTOMER-ORG PIC 9(03).
                             17  FILLER PIC 9(02).
                         13  MIC003-B044-NEXT-REC-KEY-SAIQ REDEFINES
                                 MIC003-B044-NEXT-REC-KEY.
                             17  MIC003-B044-ACCOUNT-ORG PIC 9(03).
                             17  MIC003-B044-ACCOUNT-TYPE PIC 9(03).
                             17  MIC003-B044-ACCOUNT-NBR PIC 9(16).
                             17  FILLER PIC 9(08).
                         13  FILLER PIC X(68).
                       11  FILLER REDEFINES MIC003-B044-ADDITIONAL-RESP.
                         13  MIC003-B044-END-OF-DATA-IND1 PIC X(01).
                         13  MIC003-B044-NEXT-REC-KEY1 PIC X(36).
                         13  MIC003-B044-NEXT-REC-KEY-SPTD REDEFINES
                                 MIC003-B044-NEXT-REC-KEY1.
                             17  MIC003-B044-EPT-ACCT-ORG PIC 9(03).
                             17  MIC003-B044-EPT-ACCT-TYPE PIC 9(03).
                             17  MIC003-B044-EPT-ACCT-NMBR PIC 9(16).
                             17  MIC003-B044-EPT-TRAN-DATE PIC 9(07).
                             17  MIC003-B044-EPT-TRAN-TIME PIC 9(07).
                         13  FILLER PIC X(62).
                       11  FILLER REDEFINES MIC003-B044-ADDITIONAL-RESP.
                         13  MIC003-B044-END-OF-DATA-IND2 PIC X(01).
                         13  MIC003-B044-NEXT-REC-KEY2 PIC X(44).
                         13  MIC003-B044-NEXT-REC-KEY-SMIK REDEFINES
                                 MIC003-B044-NEXT-REC-KEY2.
                             17  MIC003-B044-REC-TYP PIC 9(01).
                             17  MIC003-B044-ACC-ORG PIC 9(03).
                             17  MIC003-B044-ACC-TYPE PIC 9(03).
                             17  MIC003-B044-ACC-NBR PIC 9(16).
                             17  MIC003-B044-RELATIONSHIP PIC 9(01).
                             17  MIC003-B044-PLT-NBR PIC X(19).
                             17  MIC003-B044-ACC-SEQ PIC 9(01).
                         13  FILLER PIC X(54).
                       11  FILLER REDEFINES MIC003-B044-ADDITIONAL-RESP.
                         13  MIC003-B044-END-OF-DATA-IND3 PIC X(01).
                         13  MIC003-B044-NEXT-REC-KEY3 PIC X(44).
                         13  MIC003-B044-NEXT-REC-KEY-CCIW REDEFINES
                                 MIC003-B044-NEXT-REC-KEY3.
                             17  MIC003-B044-CUST-ORG PIC 9(03).
                             17  MIC003-B044-CUST-NBR PIC 9(16).
                             17  MIC003-B044-PLST-ORG PIC 9(03).
                             17  MIC003-B044-PLST-TYP PIC 9(03).
                             17  MIC003-B044-PLST-NBR PIC X(19).
                         13  FILLER PIC X(54).
                       11  FILLER REDEFINES MIC003-B044-ADDITIONAL-RESP.
                         13  MIC003-B044-CCTH-EOD-IND PIC X(01).
                         13  MIC003-B044-CCTH-NEXT-REC-KEY PIC X(84).
                         13  FILLER PIC X(14).
                       11  FILLER REDEFINES MIC003-B044-ADDITIONAL-RESP.
                         13  MIC003-B044-VLLC-EOD-IND PIC X(01).
                         13  MIC003-B044-NEXT-REC-KEY-VLLC.
                             17  MIC003-B044-VLLC-HIS-KEY PIC 9(16).
                             17  MIC003-B044-VLLC-FIL-IDX PIC 9(02).
                         13  FILLER PIC X(80).
                       11  FILLER REDEFINES MIC003-B044-ADDITIONAL-RESP.
                         13  MIC003-B044-ERR-BYTE-MAP PIC 9(03).
                         13  MIC003-B044-ERR-MSG PIC X(30).
                         13  FILLER PIC X(66).
                       11  FILLER REDEFINES MIC003-B044-ADDITIONAL-RESP.
                         13  FILLER PIC X(85).
                         13  MIC003-B044-RECEIVE-DATE PIC X(08).
                         13  MIC003-B044-RECEIVE-TIME PIC X(06).
                       11  FILLER REDEFINES MIC003-B044-ADDITIONAL-RESP.
                         13  MIC003-B044-TQ-END-OF-DATA-IND PIC X(01).
                         13  MIC003-B044-TQ-NEXT-REC-KEY PIC X(40).
                         13  FILLER PIC X(58).
                       11  MIC003-B045-TRACK-1-DATA-LEN PIC S9(02)
                               COMP-3.
                       11  MIC003-B045-TRACK-1-DATA PIC X(76).
                       11  MIC003-B048-ADDTL-DATA-LEN PIC S9(03) COMP-3.
                       11  MIC003-B048-ADDTL-DATA PIC X(999).
                       11  FILLER REDEFINES MIC003-B048-ADDTL-DATA.
                         13  MIC003-B048-TRANS-CODE PIC X(04).
                         13  MIC003-B048-SERVICE-CODE PIC X(08).
                         13  MIC003-B048-TERMINAL-ID PIC X(08).
                         13  MIC003-B048-REQUEST-TYPE PIC X(04).
                         13  MIC003-B048-NUMBER-OF-TRXN PIC 9(02).
                         13  MIC003-B048-SEQUENCE-ORDER PIC X(03).
                         13  MIC003-B048-NAME-EMBOSSED PIC X(30).
                         13  MIC003-B048-DATE-OF-BIRTH PIC 9(08).
                         13  MIC003-B048-ID-NUMBER PIC X(15).
                         13  MIC003-B048-OFFICE-PHONE PIC X(18).
                         13  MIC003-B048-HOUSE-PHONE PIC X(18).
                         13  MIC003-B048-SECURITY-QN PIC X(30).
                         13  MIC003-B048-MOTHER-MAIDEN-NAME REDEFINES
                                 MIC003-B048-SECURITY-QN PIC X(30).
                         13  MIC003-B048-REPORTING-REASON PIC X(01).
                         13  MIC003-B048-SECOND-ACCT-IND PIC X(01).
                         13  MIC003-B048-DATA PIC X(849).
                         13  MIC003-B048-ECOM-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-ECOM-TXN-IND PIC X(01).
                               88  MIC003-B048-ECOM-NON-INSTL VALUE
                                       SPACES.
                               88  MIC003-B048-ECOM-INSTL VALUE '2'.
                           15  MIC003-B048-ECOM-USERID PIC X(08).
                           15  MIC003-B048-ECOM-CVV2-CVC2 PIC X(03).
                           15  MIC003-B048-ECOM-INSTALMENT-PL PIC 9(03).
                           15  MIC003-B048-ECOM-PAYMENT-TERM PIC 9(02).
                           15  MIC003-B048-ECOM-INTEREST-RATE PIC
                                   9V9(05).
                           15  MIC003-B048-ECOM-SEC-DATA PIC X(90).
                           15  MIC003-B048-ECOM-SEC-DATA-V REDEFINES
                                   MIC003-B048-ECOM-SEC-DATA.
                             17  MIC003-B048-ECOM-VSEC-XID PIC X(40).
                             17  MIC003-B048-ECOM-VSEC-TRNSTAIN PIC
                                     X(40).
                             17  MIC003-B048-ECOM-VSEC-EC-IND PIC X(02).
                             17  FILLER PIC X(08).
                           15  MIC003-B048-ECOM-SEC-DATA-M REDEFINES
                                   MIC003-B048-ECOM-SEC-DATA.
                             17  MIC003-B048-ECOM-MSEC-LEVEL PIC X(02).
                             17  MIC003-B048-ECOM-MSEC-UCAF-IND PIC
                                     X(01).
                             17  MIC003-B048-ECOM-MSEC-UCAF-LEN PIC
                                     9(02).
                             17  MIC003-B048-ECOM-MSEC-UCAF-DAT PIC
                                     X(32).
                             17  MIC003-B048-ECOM-PPOL PIC X(03).
                             17  MIC003-B048-ECOM-PROG-PROTOCOL PIC
                                     X(01).
                             17  MIC003-B048-ECOM-SERVER-TXN-ID PIC
                                     X(36).
                             17  FILLER PIC X(13).
                           15  MIC003-B048-ECOM-PNBR PIC X(15).
                           15  MIC003-B048-ECOM-ADDTL-DATA PIC X(150).
                           15  MIC003-B048-ECOM-ADDTL-DATA-V REDEFINES
                                   MIC003-B048-ECOM-ADDTL-DATA.
                             17  MIC003-B048-ECOM-TKN-TXN-SEQ PIC X(01).
                             17  MIC003-B048-ECOM-POS-ENV-CODE PIC
                                     X(01).
                             17  MIC003-B048-ECOM-ORIG-TXN-ID PIC 9(15).
                             17  FILLER PIC X(133).
                           15  MIC003-B048-ECOM-ADDTL-DATA-M REDEFINES
                                   MIC003-B048-ECOM-ADDTL-DATA.
                             17  MIC003-B048-ECOM-DSRP-CRYPTO PIC X(28).
                             17  MIC003-B048-ECOM-TRACE-ID PIC X(15).
                             17  FILLER PIC X(107).
                           15  FILLER PIC X(571).
                         13  MIC003-B048-ECOM-REV-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-ECOM-REV-IND PIC X(01).
                               88  MIC003-B048-ECOM-REV-BY-SYS VALUE
                                       SPACES.
                               88  MIC003-B048-ECOM-REV-BY-CUS VALUE
                                       '3'.
                           15  FILLER PIC X(848).
                         13  MIC003-B048-CCAV-IVR-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CCAV-IVR-MOBILE PIC X(18).
                           15  FILLER PIC X(831).
                         13  MIC003-B048-GCVM-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-GCVM-OTP-REASON PIC X(02).
                           15  MIC003-B048-GCVM-TRID PIC X(11).
                           15  MIC003-B048-GCVM-TKN-REF-ID PIC X(32).
                           15  MIC003-B048-GCVM-PAN-REF-ID PIC X(32).
                           15  MIC003-B048-GCVM-LIFE-CYC-ID PIC X(15).
                           15  MIC003-B048-GCVM-PAN-SRC PIC X(02).
                           15  MIC003-B048-GCVM-DVC-NMBR PIC X(13).
                           15  FILLER PIC X(742).
                         13  MIC003-B048-SPCD-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-SPCD-IDENTIFIER PIC X(02).
                           15  MIC003-B048-SPCD-OTP-CD PIC X(08).
                           15  MIC003-B048-SPCD-OTP-EXP PIC X(19).
                           15  MIC003-B048-SPCD-OTP-REASON PIC X(02).
                           15  MIC003-B048-SPCD-TRID PIC X(11).
                           15  FILLER PIC X(807).
                         13  MIC003-B048-CCBP-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CCBP-ACCT-NMBR PIC 9(16).
                           15  FILLER PIC X(833).
                         13  MIC003-B048-SP2P-1100-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-SP2P-IND PIC X(03).
                           15  MIC003-B048-SP2P-DATA.
                             17  MIC003-B048-SP2P-STATUS PIC X(01).
                             17  MIC003-B048-SP2P-GL-REFERENCE PIC
                                     X(30).
                           15  MIC003-B048-SP2P-DATA2 REDEFINES
                                   MIC003-B048-SP2P-DATA.
                             17  MIC003-B048-SP2P-TXN-EXPDATE PIC 9(08).
                             17  FILLER PIC X(23).
                           15  MIC003-B048-SP2P-TC-CODE PIC X(04).
                           15  MIC003-B048-SP2P-TC-CODE-NUM REDEFINES
                                   MIC003-B048-SP2P-TC-CODE PIC 9(04).
                           15  MIC003-B048-SP2P-DESCRIPTION PIC X(35).
                           15  MIC003-B048-SP2P-MYC-IND PIC X(1).
                           15  MIC003-B048-SP2P-RR PIC X(20).
                           15  MIC003-B048-SP2P-OPD PIC X(20).
                           15  MIC003-B048-SP2P-SNM PIC X(80).
                           15  FILLER PIC X(655).
                         13  MIC003-B048-VCIC-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-VCIC-CUS-NBR1 PIC X(19).
                           15  MIC003-B048-VCIC-ID-TY1 PIC X(02).
                           15  MIC003-B048-VCIC-CUS-NBR2 PIC X(19).
                           15  MIC003-B048-VCIC-ID-TY2 PIC X(02).
                           15  FILLER PIC X(807).
                         13  MIC003-B048-PYMT-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-PYMT-ACCT-NMBR PIC 9(16).
                           15  MIC003-B048-PYMT-MYCLR-DATA.
                             17  MIC003-B048-PYMT-MYCLR-TXN-IND PIC
                                     X(01).
                             17  MIC003-B048-PYMT-MYCLR-RR PIC X(20).
                             17  MIC003-B048-PYMT-MYCLR-DESC PIC X(20).
                             17  MIC003-B048-PYMT-MYCLR-NAME PIC X(80).
                             17  MIC003-B048-PYMT-FROM-ACCT PIC X(19).
                             17  MIC003-B048-PYMT-TRXN-TYPE PIC X(03).
                             17  MIC003-B048-PYMT-INDICATOR PIC X(04).
                             17  MIC003-B048-PYMT-MTID PIC X(28).
                             17  MIC003-B048-PYMT-DUPL-FLAG PIC X(01).
                             17  MIC003-B048-PYMT-SAF-IND PIC X(01).
                             17  MIC003-B048-PYMT-BIZMSG-IDR PIC X(30).
                             17  MIC003-B048-PYMT-MER-IND PIC X(01).
                           15  FILLER PIC X(625).
                         13  MIC003-B048-PRPP-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-PRPP-ACCT-NMBR PIC 9(16).
                           15  MIC003-B048-PRPP-MYCLR-DATA.
                             17  MIC003-B048-PRPP-MYCLR-TXN-IND PIC
                                     X(01).
                             17  MIC003-B048-PRPP-MYCLR-RR PIC X(140).
                             17  MIC003-B048-PRPP-MYCLR-DESC PIC X(140).
                             17  MIC003-B048-PRPP-MYCLR-NAME PIC X(140).
                             17  MIC003-B048-PRPP-FROM-ACCT PIC X(19).
                             17  MIC003-B048-PRPP-TRXN-TYPE PIC X(03).
                             17  MIC003-B048-PRPP-INDICATOR PIC X(04).
                             17  MIC003-B048-PRPP-MTID PIC X(28).
                             17  MIC003-B048-PRPP-DUPL-FLAG PIC X(01).
                             17  MIC003-B048-PRPP-SAF-IND PIC X(01).
                             17  MIC003-B048-PRPP-BIZMSG-IDR PIC X(30).
                             17  MIC003-B048-PRPP-RTP-TRANS-IND PIC
                                     X(01).
                             17  MIC003-B048-PRPP-EX-PYM-DTL PIC X(250).
                           15  FILLER PIC X(75).
                         13  MIC003-B048-CPCG-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CPCG-NEW-PIN-BLK PIC X(16).
                           15  FILLER PIC X(833).
                         13  MIC003-B048-PINC-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-PINC-NEW-PIN-BLK PIC X(16).
                           15  FILLER PIC X(833).
                         13  MIC003-B048-CPVU-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CPVU-CNTLES-LMT PIC 9(11).
                           15  FILLER PIC X(838).
                         13  MIC003-B048-CCOP-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CCOP-PYMT-METHOD PIC 9(01).
                           15  MIC003-B048-CCOP-DB-NMBR PIC 9(16).
                           15  MIC003-B048-CCOP-ACCT-NMBR PIC 9(16).
                           15  FILLER PIC X(816).
                         13  MIC003-B048-CCCP-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CCCP-CRLIMIT1 PIC 9(09).
                           15  MIC003-B048-CCCP-CRLIMIT2 PIC 9(09).
                           15  MIC003-B048-CCCP-CRLINE PIC 9(11).
                           15  MIC003-B048-CCCP-RTLLIMIT PIC 9(10).
                           15  MIC003-B048-CCCP-CTD-RTLLIMIT PIC 9(15).
                           15  MIC003-B048-CCCP-CSHLIMIT PIC 9(10).
                           15  MIC003-B048-CCCP-CTD-CSHLIMIT PIC 9(15).
                           15  MIC003-B048-CCCP-BNM-CAT-CDE PIC 9(02).
                           15  MIC003-B048-CCCP-BNM-REASON PIC X(200).
                           15  MIC003-B048-CCCP-BPP PIC 9(09)V99.
                           15  MIC003-B048-CCCP-BSP PIC 9(09)V99.
                           15  MIC003-B048-CCCP-TTL-PROFIT PIC 9(09)V99.
                           15  MIC003-B048-CCCP-UNEARNED-PFT PIC
                                   9(09)V99.
                           15  FILLER PIC X(524).
                         13  MIC003-B048-MTKQ-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-MTKQ-INQ-PURPOSE PIC X(01).
                           15  MIC003-B048-MTKQ-USER-ID PIC X(50).
                           15  MIC003-B048-MTKQ-USER-NAME PIC X(60).
                           15  FILLER PIC X(738).
                         13  MIC003-B048-CCCT-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CCCT-CRLIMIT1 PIC 9(09).
                           15  MIC003-B048-CCCT-CRLIMIT1-EFF PIC 9(08).
                           15  MIC003-B048-CCCT-CRLIMIT1-EXP PIC 9(08).
                           15  MIC003-B048-CCCT-CRLIMIT2 PIC 9(09).
                           15  MIC003-B048-CCCT-CRLIMIT2-EFF PIC 9(08).
                           15  MIC003-B048-CCCT-CRLIMIT2-EXP PIC 9(08).
                           15  MIC003-B048-CCCT-CRLINE PIC 9(11).
                           15  MIC003-B048-CCCT-CRLINE-EFF PIC 9(08).
                           15  MIC003-B048-CCCT-CRLINE-EXP PIC 9(08).
                           15  MIC003-B048-CCCT-RTLLIMIT PIC 9(10).
                           15  MIC003-B048-CCCT-CTD-RTLLIMIT PIC 9(15).
                           15  MIC003-B048-CCCT-CSHLIMIT PIC 9(10).
                           15  MIC003-B048-CCCT-CTD-CSHLIMIT PIC 9(15).
                           15  MIC003-B048-CCCT-PLIMIT-EFF PIC 9(08).
                           15  MIC003-B048-CCCT-PLIMIT-EXP PIC 9(08).
                           15  FILLER PIC X(706).
                         13  MIC003-B048-MAAQ-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-AQ-CR-IC PIC X(25).
                           15  MIC003-B048-AQ-CR-IC-TYPE PIC X(02).
                           15  FILLER PIC X(822).
                         13  MIC003-B048-MTKP-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-MTKP-VISA-TKN-RID PIC X(32).
                           15  MIC003-B048-MTKP-MC-CORREL-ID PIC X(14).
                           15  FILLER PIC X(803).
                         13  MIC003-B048-CCMC-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CCMC-HOME-PHONE PIC X(18).
                           15  MIC003-B048-CCMC-MOBILE-PHONE PIC X(18).
                           15  MIC003-B048-CCMC-OFFICE-PHONE PIC X(18).
                           15  MIC003-B048-CCMC-EMAIL-ADDRESS PIC X(50).
                           15  MIC003-B048-CCMC-NAME-1 PIC X(30).
                           15  MIC003-B048-CCMC-NAME-2 PIC X(30).
                           15  MIC003-B048-CCMC-NAME-3 PIC X(30).
                           15  MIC003-B048-CCMC-ADDR-1 PIC X(30).
                           15  MIC003-B048-CCMC-ADDR-2 PIC X(30).
                           15  MIC003-B048-CCMC-CITY PIC X(28).
                           15  MIC003-B048-CCMC-STATE PIC X(2).
                           15  MIC003-B048-CCMC-ZIP-CODE PIC X(9).
                           15  MIC003-B048-CCMC-ADDL-ADDR-1 PIC X(30).
                           15  MIC003-B048-CCMC-ADDL-ADDR-2 PIC X(30).
                           15  MIC003-B048-CCMC-ADDL-ADDR-3 PIC X(30).
                           15  MIC003-B048-CCMC-ADDL-CITY PIC X(30).
                           15  MIC003-B048-CCMC-ADDL-ZIP PIC X(22).
                           15  MIC003-B048-CCMC-ADDL-EXP-DATE PIC 9(08).
                           15  FILLER PIC X(406).
                         13  MIC003-B048-CPRQ-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CPRQ-CARD-ACTION PIC 9(01).
                           15  MIC003-B048-CPRQ-USER-ID PIC X(08).
                           15  FILLER PIC X(840).
                         13  MIC003-B048-COFU-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-COFU-FLAG PIC X(01).
                           15  MIC003-B048-COFU-START-DATE PIC 9(08).
                           15  MIC003-B048-COFU-END-DATE PIC 9(08).
                           15  FILLER PIC X(832).
                         13  MIC003-B048-CCFU-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CCFU-FLAG PIC X(01).
                           15  FILLER PIC X(848).
                         13  MIC003-B048-CCPS-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CCPS-STMT-CYCLE PIC X(02).
                               88  MIC003-VALID-CCPS-STMT-CYCLE VALUE
                                       '  ' '02' THRU '12'.
                           15  MIC003-B048-SCLT-REL PIC X(01).
                           15  MIC003-B048-SCLS-STMT-CYCLE-YM PIC 9(06).
                           15  FILLER PIC X(840).
                         13  MIC003-B048-MTKA-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-KA-MC-PAID PIC X(48).
                           15  MIC003-B048-KA-USR-ID PIC X(50).
                           15  FILLER PIC X(751).
                         13  MIC003-B048-MTAM-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-AM-MC-PAID PIC X(48).
                           15  MIC003-B048-AM-CMNT-TXT PIC X(50).
                           15  MIC003-B048-AM-RSN-CODE PIC X(01).
                           15  MIC003-B048-AM-USR-ID PIC X(50).
                           15  MIC003-B048-AM-CR-NAME PIC X(60).
                           15  MIC003-B048-AM-ORG PIC X(50).
                           15  MIC003-B048-AM-CR-PHONE PIC X(18).
                           15  FILLER PIC X(572).
                         13  MIC003-B048-MTKM-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-TM-TOKEN PIC X(19).
                           15  MIC003-B048-TM-ACTION PIC X(01).
                           15  MIC003-B048-TM-ACTION-DATE PIC 9(08).
                           15  MIC003-B048-TM-REPL-CARD PIC X(19).
                           15  MIC003-B048-TM-REPL-EXPIRY PIC 9(04).
                           15  MIC003-B048-TM-REPL-CARD-SEQ PIC 9(03).
                           15  MIC003-B048-TM-NOTIFY-SVC PIC X(01).
                           15  MIC003-B048-TM-TKN-REF-ID PIC X(32).
                           15  FILLER PIC X(762).
                         13  MIC003-B048-MTIM-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-IM-EXCL-DEL-IND PIC X(01).
                           15  MIC003-B048-IM-INCL-DVC-IND PIC X(01).
                           15  MIC003-B048-IM-EXCL-TKN-IND PIC X(01).
                           15  MIC003-B048-IM-TKN-STS-CODE PIC X(01).
                           15  MIC003-B048-IM-USR-ID PIC X(50).
                           15  MIC003-B048-IM-USR-NAME PIC X(60).
                           15  MIC003-B048-IM-ORG PIC X(50).
                           15  MIC003-B048-IM-PHONE PIC X(18).
                           15  FILLER PIC X(667).
                         13  MIC003-B048-AUTH-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-AUTH-REVERSAL-DATA PIC X(42).
                           15  MIC003-B048-AUTH-FILLER PIC X(712).
                           15  MIC003-B048-AUTH-REV-ADD-DATA REDEFINES
                                   MIC003-B048-AUTH-FILLER.
                             17  MIC003-B048-AUTH-REV-BIZMSGID PIC
                                     X(35).
                             17  MIC003-B048-AUTH-REV-GL-REF PIC X(30).
                             17  FILLER PIC X(647).
                           15  MIC003-B048-PARTIAL-APPR-IND PIC X(01).
                               88  MIC003-B048-SUPP-PARTIAL-APPR VALUE
                                       'Y'.
                           15  FILLER PIC X(94).
                         13  MIC003-B048-CCAA-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CCAA-CUST-ORG PIC 9(03).
                           15  MIC003-B048-CCAA-CUST-NMBR PIC 9(16).
                           15  MIC003-B048-CCAA-CARD-TYPE PIC 9(03).
                           15  MIC003-B048-CCAA-ACCOUNT-NMBR PIC 9(16).
                           15  MIC003-B048-CCAA-NAME-LINE-1 PIC X(30).
                           15  MIC003-B048-CCAA-NAME-LINE-2 PIC X(30).
                           15  MIC003-B048-CCAA-SHORT-NAME PIC X(15).
                           15  MIC003-B048-CCAA-ADD-LINE-1 PIC X(30).
                           15  MIC003-B048-CCAA-ADD-LINE-2 PIC X(30).
                           15  MIC003-B048-CCAA-CITY PIC X(28).
                           15  MIC003-B048-CCAA-ST-CNTY PIC X(02).
                           15  MIC003-B048-CCAA-ZIP-CD PIC X(09).
                           15  MIC003-B048-CCAA-HOME-PHONE PIC X(18).
                           15  MIC003-B048-CCAA-HANDPHONE PIC X(18).
                           15  MIC003-B048-CCAA-EMAIL PIC X(30).
                           15  MIC003-B048-CCAA-CREDIT-LINE PIC 9(11).
                           15  MIC003-B048-CCAA-EMPLOYER PIC X(30).
                           15  MIC003-B048-CCAA-WORK-PHONE PIC X(18).
                           15  MIC003-B048-CCAA-BILLING-CYCLE PIC 9(02).
                           15  MIC003-B048-CCAA-SEX PIC 9(01).
                           15  MIC003-B048-CCAA-INCOME PIC 9(09).
                           15  MIC003-B048-CCAA-BEHAV-SCORE PIC 9(03).
                           15  MIC003-B048-CCAA-HOME-OWNER PIC 9(01).
                           15  MIC003-B048-CCAA-TYP-OF-RES PIC X(02).
                           15  MIC003-B048-CCAA-ACORN-CODE PIC X(04).
                           15  MIC003-B048-CCAA-LEZ-CODE PIC X(04).
                           15  MIC003-B048-CCAA-BANK-ACCT-IND PIC X(02).
                           15  MIC003-B048-CCAA-MARITAL-STS PIC 9(01).
                           15  MIC003-B048-CCAA-NBR-OF-DEPS PIC 9(02).
                           15  MIC003-B048-CCAA-OCCPN-CODE PIC X(04).
                           15  MIC003-B048-CCAA-PER-OCCPN PIC 9(04).
                           15  MIC003-B048-CCAA-CUST-CLASS PIC X(02).
                           15  MIC003-B048-CCAA-EMPLOYER-CODE PIC X(04).
                           15  MIC003-B048-CCAA-CRT-LIABLE PIC X(01).
                           15  MIC003-B048-CCAA-SMSA PIC 9(04).
                           15  MIC003-B048-CCAA-CENSUS PIC 9(07).
                           15  MIC003-B048-CCAA-EMPL-TYP PIC X(03).
                           15  MIC003-B048-CCAA-MSIC-2008 PIC X(05).
                           15  MIC003-B048-CCAA-OKU-IND PIC X(01).
                           15  MIC003-B048-CCAA-LAST-IC PIC X(25).
                           15  MIC003-B048-CCAA-DUP-STMT-ORG PIC 9(03).
                           15  MIC003-B048-CCAA-DUP-STMT-NBR PIC 9(16).
                           15  MIC003-B048-CCAA-ACC-CYCLE PIC 9(02).
                           15  MIC003-B048-CCAA-AGENT-BANK PIC 9(05).
                           15  MIC003-B048-CCAA-SH-NAME PIC X(15).
                           15  MIC003-B048-CCAA-USER-CODE-1 PIC X(02).
                           15  MIC003-B048-CCAA-USER-CODE-2 PIC X(02).
                           15  MIC003-B048-CCAA-USER-CODE-3 PIC X(02).
                           15  MIC003-B048-CCAA-USER-CODE-6 PIC X(02).
                           15  MIC003-B048-CCAA-CRLIMIT PIC 9(11).
                           15  MIC003-B048-CCAA-SRC-INC PIC X(03).
                           15  MIC003-B048-CCAA-SRC-INC-OTH PIC X(50).
                           15  MIC003-B048-CCAA-RELATIONSHIP PIC X(01).
                           15  MIC003-B048-CCAA-EMBOSS-NAME1 PIC X(26).
                           15  MIC003-B048-CCAA-EMBOSS-NAME2 PIC X(26).
                           15  MIC003-B048-CCAA-ACCT-ORG PIC 9(03).
                           15  MIC003-B048-CCAA-ACCT-TYPE PIC 9(03).
                           15  MIC003-B048-CCAA-ACCT-NMBR PIC 9(16).
                           15  MIC003-B048-CCAA-ACCT-CURR-CD PIC 9(03).
                           15  MIC003-B048-CCAA-PLT-CYCLE PIC 9(02).
                           15  MIC003-B048-CCAA-CUSTOMER-ORG PIC 9(03).
                           15  MIC003-B048-CCAA-CUSTOMER-ID PIC 9(16).
                           15  MIC003-B048-CCAA-SUP-CUST-ORG PIC 9(03).
                           15  MIC003-B048-CCAA-SUP-CUST-ID PIC 9(16).
                           15  MIC003-B048-CCAA-USER-DATA-2 PIC X(20).
                           15  MIC003-B048-CCAA-PRD-TYP PIC X(01).
                           15  MIC003-B048-CCAA-CUS-TYP PIC X(01).
                           15  MIC003-B048-CCAA-PRN-DAT-FLD-1 PIC X(20).
                           15  MIC003-B048-CCAA-PRN-DAT-FLD-2 PIC X(20).
                           15  MIC003-B048-CCAA-PRD-IND-1 PIC X(01).
                           15  MIC003-B048-CCAA-PRD-IND-2 PIC X(01).
                           15  MIC003-B048-CCAA-PRD-IND-3 PIC X(01).
                           15  MIC003-B048-CCAA-OTH-IND PIC 9(01).
                           15  FILLER PIC X(124).
                         13  MIC003-B048-CASH-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CASH-GL-REFERENCE PIC X(30).
                           15  MIC003-B048-CASH-TC-CODE PIC X(04).
                           15  MIC003-B048-CASH-TC-CODE-NUM REDEFINES
                                   MIC003-B048-CASH-TC-CODE PIC 9(04).
                           15  MIC003-B048-CASH-DESCRIPTION PIC X(35).
                           15  MIC003-B048-CASH-MYCLR-TXN-IND PIC X(01).
                           15  MIC003-B048-CASH-MYCLR-RR PIC X(20).
                           15  MIC003-B048-CASH-MYCLR-DESC PIC X(20).
                           15  MIC003-B048-CASH-TO-ACCT PIC X(19).
                           15  MIC003-B048-CASH-DOC-NO PIC X(20).
                           15  MIC003-B048-CASH-TRXN-TYPE PIC X(03).
                           15  FILLER PIC X(697).
                         13  MIC003-B048-CCRT-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-CCRT-GL-REF PIC X(30).
                           15  MIC003-B048-CCRT-RA-TC PIC X(04).
                           15  MIC003-B048-CCRT-RA-AMT PIC 9(10)V99.
                           15  MIC003-B048-CCRT-RF-TC PIC X(04).
                           15  MIC003-B048-CCRT-RF-AMT PIC 9(05)V99.
                           15  MIC003-B048-CCRT-SD-TC PIC X(04).
                           15  MIC003-B048-CCRT-SD-AMT PIC 9(05)V99.
                           15  MIC003-B048-CCRT-MC-TC PIC X(04).
                           15  MIC003-B048-CCRT-MC-AMT PIC 9(05)V99.
                           15  MIC003-B048-CCRT-DESCRIPTION PIC X(35).
                           15  MIC003-B048-CCRT-SC-TC PIC X(04).
                           15  MIC003-B048-CCRT-SC-AMT PIC 9(05)V99.
                           15  MIC003-B048-CCRT-CPF-TC PIC X(04).
                           15  MIC003-B048-CCRT-CPF-AMT PIC 9(05)V99.
                           15  MIC003-B048-CCRT-GST-RF-CD PIC X(03).
                           15  MIC003-B048-CCRT-GST-RF-AMT PIC 9(05)V99.
                           15  MIC003-B048-CCRT-GST-SD-CD PIC X(03).
                           15  MIC003-B048-CCRT-GST-SD-AMT PIC 9(05)V99.
                           15  MIC003-B048-CCRT-GST-MC-CD PIC X(03).
                           15  MIC003-B048-CCRT-GST-MC-AMT PIC 9(05)V99.
                           15  MIC003-B048-CCRT-GST-SC-CD PIC X(03).
                           15  MIC003-B048-CCRT-GST-SC-AMT PIC 9(05)V99.
                           15  MIC003-B048-CCRT-GST-CPF-CD PIC X(03).
                           15  MIC003-B048-CCRT-GST-CPF-AMT PIC
                                   9(05)V99.
                           15  MIC003-B048-CCRT-RF-DESC PIC X(35).
                           15  MIC003-B048-CCRT-SD-DESC PIC X(35).
                           15  MIC003-B048-CCRT-MC-DESC PIC X(35).
                           15  MIC003-B048-CCRT-SC-DESC PIC X(35).
                           15  MIC003-B048-CCRT-CPF-DESC PIC X(35).
                           15  MIC003-B048-CCRT-FROM-ACCT PIC X(19).
                           15  MIC003-B048-CCRT-TRXN-TYPE PIC X(03).
                           15  MIC003-B048-CCRT-DOC-NO PIC X(09).
                           15  FILLER PIC X(457).
                         13  MIC003-B048-RTL-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-RTL-GL-REFERENCE PIC X(30).
                           15  MIC003-B048-RTL-TC-CODE PIC X(04).
                           15  MIC003-B048-RTL-TC-CODE-NUM REDEFINES
                                   MIC003-B048-RTL-TC-CODE PIC 9(04).
                           15  MIC003-B048-RTL-DESCRIPTION PIC X(35).
                           15  MIC003-B048-RTL-DOC-NO PIC X(20).
                           15  MIC003-B048-RTL-GST-CDE PIC X(03).
                           15  MIC003-B048-RTL-GST-AMT PIC 9(5)V99.
                           15  MIC003-B048-RTL-FROM-ACCT PIC X(19).
                           15  MIC003-B048-RTL-TRXN-TYPE PIC X(03).
                           15  MIC003-B048-RTL-INDICATOR PIC X(04).
                           15  MIC003-B048-RTL-MTID PIC X(28).
                           15  MIC003-B048-RTL-MYCLR-TXN-IND PIC X(01).
                           15  MIC003-B048-RTL-MYCLR-RR PIC X(20).
                           15  MIC003-B048-RTL-MYCLR-DESC PIC X(20).
                           15  MIC003-B048-RTL-MYCLR-NAME PIC X(80).
                           15  FILLER PIC X(575).
                         13  MIC003-B048-SCIK-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-SCIK-CUSTOMER-ID PIC 9(16).
                           15  FILLER PIC X(833).
                         13  MIC003-B048-SCAP-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-SCAP-FUNCTION-REQ PIC X(05).
                           15  MIC003-B048-SCAP-USERID PIC X(08).
                           15  FILLER PIC X(836).
                         13  MIC003-B048-NBPS-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-NBPS-TRX-IND PIC X(04).
                           15  MIC003-B048-NBPS-BILLER-CODE PIC X(10).
                           15  MIC003-B048-NBPS-BILLER-NAME PIC X(40).
                           15  MIC003-B048-NBPS-RR-NUMBER1 PIC X(20).
                           15  MIC003-B048-NBPS-REF-NUM PIC X(20).
                           15  MIC003-B048-NBPS-GL-REF-NUM PIC X(30).
                           15  MIC003-B048-NBPS-MER-IND PIC X(01).
                           15  MIC003-B048-NBPS-BIZ-MSD-ID PIC X(35).
                           15  MIC003-B048-NBPS-RTP-TRANS-IND PIC X(01).
                           15  FILLER PIC X(688).
                         13  MIC003-B048-SCIQ-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-SCIQ-CUST-ORG PIC 9(03).
                           15  MIC003-B048-SCIQ-CUST-NBR PIC 9(16).
                           15  MIC003-B048-SCIQ-CUST-ID PIC X(25).
                           15  MIC003-B048-SCIQ-CUST-ID-TYP PIC X(03).
                           15  FILLER PIC X(802).
                         13  MIC003-B048-SAIQ-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-SAIQ-CUST-ORG PIC 9(03).
                           15  MIC003-B048-SAIQ-CUST-NBR PIC 9(16).
                           15  FILLER PIC X(830).
                         13  MIC003-B048-SPPT-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-SPPT-ACCT-ORG PIC 9(03).
                           15  MIC003-B048-SPPT-ACCT-TYPE PIC 9(03).
                           15  MIC003-B048-SPPT-ACCT-NMBR PIC 9(16).
                           15  MIC003-B048-SPPT-TRAN-DATE PIC 9(08).
                           15  MIC003-B048-SPPT-TRAN-TIME PIC 9(07).
                           15  MIC003-B048-SPPT-USERID PIC X(08).
                           15  MIC003-B048-SPPT-REQUEST-TYPE PIC X(01).
                           15  MIC003-B048-SPPT-REQUEST-DTLS PIC X(803).
                           15  MIC003-B048-SPPT-PRE-TERM REDEFINES
                                   MIC003-B048-SPPT-REQUEST-DTLS.
                             17  MIC003-B048-SPPT-FEE-IND PIC X(01).
                             17  MIC003-B048-SPPT-DISPUTE-IND PIC X(01).
                             17  MIC003-B048-SPPT-P-APPLID PIC X(20).
                             17  FILLER PIC X(781).
                           15  MIC003-B048-SPPT-SALES-COMPL REDEFINES
                                   MIC003-B048-SPPT-REQUEST-DTLS.
                             17  MIC003-B048-SPPT-SSS-NMBR PIC 9(10).
                             17  MIC003-B048-SPPT-ALP-KEY PIC X(16).
                             17  MIC003-B048-SPPT-AG-BANK PIC 9(05).
                             17  MIC003-B048-SPPT-S-APPLID PIC X(20).
                             17  FILLER PIC X(752).
                           15  MIC003-B048-SPPT-DEL-DTLS REDEFINES
                                   MIC003-B048-SPPT-REQUEST-DTLS.
                             17  MIC003-B048-SPPT-ITEM-PRICE PIC
                                     9(09)V99.
                             17  MIC003-B048-SPPT-AUT-CODE PIC X(6).
                             17  MIC003-B048-SPPT-MER-ORGN PIC 9(3).
                             17  MIC003-B048-SPPT-MER-NMBR PIC 9(15).
                             17  MIC003-B048-SPPT-MCC PIC 9(5).
                             17  MIC003-B048-SPPT-CUR-CODE PIC 9(3).
                             17  MIC003-B048-SPPT-CUR-EXPN PIC 9(1).
                             17  MIC003-B048-SPPT-D-APPLID PIC X(20).
                             17  FILLER PIC X(739).
                         13  MIC003-B048-SPTD-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-SPTD-STATUS-IND PIC X(01).
                           15  FILLER PIC X(848).
                         13  MIC003-B048-SCTF-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-SCTF-PLASTIC-NBR PIC X(19).
                           15  MIC003-B048-SCTF-EFF-DATE PIC 9(08).
                           15  MIC003-B048-SCTF-EXP-DATE PIC 9(04).
                           15  MIC003-B048-SCTF-USER-ID PIC X(08).
                           15  FILLER PIC X(810).
                         13  MIC003-B048-SICR-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-SICR-COLL-BRANCH PIC 9(05).
                           15  MIC003-B048-SICR-USER-ID PIC X(08).
                           15  FILLER PIC X(836).
                         13  MIC003-B048-SMIK-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-SMIK-CUST-ORG PIC 9(03).
                           15  MIC003-B048-SMIK-CUST-NBR PIC 9(16).
                           15  FILLER PIC X(830).
                         13  MIC003-B048-SMCS-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-SMCS-TNG-MFG-NBR PIC 9(16).
                           15  MIC003-B048-SMCS-REQ-TYPE PIC X(01).
                           15  MIC003-B048-SMCS-REQ-INP-DET PIC X(16).
                           15  MIC003-B048-SMCS-USER-ID PIC X(08).
                           15  FILLER PIC X(808).
                         13  MIC003-B048-SPTE-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-SPTE-TXN-IND PIC X(01).
                           15  MIC003-B048-SPTE-USERID PIC X(08).
                           15  MIC003-B048-SPTE-CVV-CVC PIC 9(03).
                           15  MIC003-B048-SPTE-INSTALMENT-PL PIC 9(03).
                           15  MIC003-B048-SPTE-PAYMENT-TERM PIC 9(02).
                           15  MIC003-B048-SPTE-INTEREST-RATE PIC
                                   9V9(05).
                           15  MIC003-B048-SPTE-APPLID PIC X(20).
                           15  MIC003-B048-SPTE-BUN-CL-IND PIC X(01).
                           15  FILLER PIC X(805).
                         13  MIC003-B048-MSIC-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-MSIC-CODE PIC X(05).
                           15  FILLER PIC X(844).
                         13  MIC003-B048-VMI1-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-VMI1-INSTL-PLAN PIC 9(03).
                           15  FILLER PIC X(846).
                         13  MIC003-B048-VLLC-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-VLLC-ORG-NBR PIC 9(03).
                           15  MIC003-B048-VLLC-DTE-FROM PIC 9(08).
                           15  MIC003-B048-VLLC-DTE-TO PIC 9(08).
                           15  FILLER PIC X(830).
                         13  MIC003-B048-VLIC-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-VLIC-HIST-KEY PIC X(16).
                           15  MIC003-B048-VLIC-FILE-IDX PIC 9(02).
                           15  FILLER PIC X(831).
                         13  MIC003-B048-VCIH-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-VCIH-CCY PIC 9(03).
                           15  MIC003-B048-VCIH-STMT-DTE PIC 9(08).
                           15  FILLER PIC X(838).
                         13  MIC003-B048-VMDR-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-VMDR-CCY PIC 9(03).
                           15  FILLER PIC X(846).
                         13  MIC003-B048-VMIC-DATA REDEFINES
                                 MIC003-B048-DATA.
                           15  MIC003-B048-VMIC-CNT-ID PIC X(06).
                           15  FILLER PIC X(843).
                       11  MIC003-B049-TRXN-CURR-CODE PIC 9(03).
                       11  MIC003-B052-PIN-DATA PIC X(16).
                       11  MIC003-B054-AMOUNT-ADDTL-LEN PIC S9(03)
                               COMP-3.
                       11  MIC003-B054-AMOUNT-ADDTL-DATA PIC X(120).
                       11  FILLER REDEFINES
                               MIC003-B054-AMOUNT-ADDTL-DATA.
                         13  MIC003-B054-AMOUNT-ADDTL OCCURS 6 TIMES.
                           15  MIC003-B054-ACCOUNT-TYPE PIC 9(02).
                           15  MIC003-B054-AMOUNT-TYPE PIC 9(02).
                           15  MIC003-B054-CURRENCY-CODE PIC X(03).
                           15  MIC003-B054-AMOUNT-CR-DR PIC X(01).
                           15  MIC003-B054-AMOUNT-ADDITIONAL PIC 9(12).
                       11  MIC003-B056-ORIGINAL-DATA-LEN PIC S9(02)
                               COMP-3.
                       11  MIC003-B056-ORIGINAL-DATA.
                         13  MIC003-B056-ORIG-MTI PIC 9(04).
                         13  MIC003-B056-ORIG-STN PIC 9(06).
                         13  MIC003-B056-ORIG-LDT PIC 9(12).
                         13  MIC003-B056-ORIG-AII-LEN PIC 9(02).
                         13  MIC003-B056-ORIG-AII PIC 9(11).
                     09  MIC003-VAR-LENGTH-QUEUE-REC.
                       11  MIC003-B060-OUTPUT-DATA-1-LEN PIC S9(03)
                               COMP-3.
                       11  MIC003-B060-OUTPUT-DATA-1 PIC X(999).
                       11  FILLER REDEFINES MIC003-B060-OUTPUT-DATA-1.
                         13  MIC003-B060-CCAA-CVV PIC X(04).
                         13  FILLER PIC X(995).
                       11  FILLER REDEFINES MIC003-B060-OUTPUT-DATA-1.
                         13  MIC003-B060-CCAV-CRD-ACTN PIC 9(01).
                         13  MIC003-B060-CCAV-IVR-ACTN-DTE PIC 9(08).
                         13  FILLER PIC X(990).
                       11  FILLER REDEFINES MIC003-B060-OUTPUT-DATA-1.
                         13  MIC003-B060-CCTH-OUT PIC X(124) OCCURS 8
                                 TIMES.
                         13  FILLER PIC X(07).
      * DE60 RESPONSE - CCPS - MIC002-STATEMENT-INQ-REC
                       11  ML60-CCPS REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-SECOND-ACCT-IND  PIC X(01).
                         13  MIC002-HOST-DATE-TIME  PIC 9(14).
                         13  MIC002-CR-LIMIT     PIC 9(09).
                         13  MIC002-CUR-BAL      PIC 9(09)V99.
                         13  MIC002-CUR-BAL-IND  PIC X(01).
                         13  MIC002-PREV-BAL     PIC 9(09)V99.
                         13  MIC002-PREV-BAL-IND  PIC X(01).
                         13  MIC002-OTHER-HEADER  PIC X(29).
                         13  MIC002-NO-OF-TRANS-DTL  PIC 9(02).
                         13  MIC002-TX-POST-DATE  PIC X(08).
                         13  MIC002-TX-DATE      PIC X(08).
                         13  MIC002-TX-DESC      PIC X(40).
                         13  MIC002-TX-AMT       PIC X(12).
                         13  MIC002-TX-AMT-IND   PIC X(01).
                         13  MIC002-TX-REF-NO    PIC X(23).
                         13  MIC002-CARD-NMBR    PIC X(19).
                         13  MIC002-TX-CODE      PIC 9(04).
                         13  MIC002-MCC          PIC 9(04).
                         13  MIC002-POS-MODE     PIC X(02).
                         13  MIC002-XBORDER-AMT  PIC S9(07)V99.
                         13  MIC002-MARKUP-AMT   PIC S9(07)V99.
                         13  MIC002-CCA-AMT      PIC S9(07)V99.
                         13  FILLER              PIC X(15).
                         13  FILLER              PIC X(757).
      * DE60 RESPONSE - CCBP - MIC002-BONUS-REDEMPTION-REC
                       11  ML60-CCBP REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-BP-UPDATED-BALANCE  PIC 9(10).
                         13  MIC002-BP-UPDATED-USED-CTD  PIC 9(10).
                         13  FILLER              PIC X(979).
      * DE60 RESPONSE - PYMT - MIC002-PYMT-RESP-INFO-REC
                       11  ML60-PYMT REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-PYMT-BANK-CODE  PIC 9(02).
                         13  MIC002-PYMT-BRANCH-CODE  PIC 9(05).
                         13  MIC002-PYMT-GL-REFERENCE  PIC X(20).
                         13  MIC002-PYMT-REASON-CODE  PIC X(02).
                         13  MIC002-PYMT-P2P-TRANS-DESC  PIC X(53).
                         13  MIC002-PYMT-TC-CODE  PIC X(04).
                         13  MIC002-PYMT-CURR-BALANCE  PIC 9(10)V99.
                         13  MIC002-PYMT-CURR-BALANCE-IND  PIC X(01).
                         13  MIC002-PYMT-CO-AVL-CRE  PIC 9(12)V99.
                         13  MIC002-PYMT-CO-AVL-CRE-IND  PIC X(01).
                         13  MIC002-PYMT-CR-AVL-CRE  PIC 9(12)V99.
                         13  MIC002-PYMT-CR-AVL-CRE-IND  PIC X(01).
                         13  MIC002-PYMT-CM-AVL-CRE  PIC 9(12)V99.
                         13  MIC002-PYMT-CM-AVL-CRE-IND  PIC X(01).
                         13  MIC002-PYMT-PL-AVL-CRE  PIC 9(12)V99.
                         13  MIC002-PYMT-PL-AVL-CRE-IND  PIC X(01).
                         13  MIC002-PYMT-ACCT-NAME  PIC X(140).
                         13  MIC002-PYMT-ACCT-TYP  PIC X(04).
                         13  MIC002-PYMT-RSDN-ST  PIC X(01).
                         13  MIC002-PYMT-PROD-TYP  PIC X(01).
                         13  MIC002-PYMT-SHARIAH-CMPL  PIC X(01).
                         13  MIC002-PYMT-DETAILS  PIC X(01).
                         13  MIC002-PYMT-CUST-CATEGORY  PIC X(03).
                         13  FILLER              PIC X(689).
      * DE60 RESPONSE - ECOM - MIC002-ECOM-RESP-INFO-REC
                       11  ML60-ECOM REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-EI-INSTL-PLAN  PIC 9(03).
                         13  MIC002-EI-PAY-TERM  PIC 9(02).
                         13  MIC002-EI-COMPUTE-METHOD  PIC 9(01).
                         13  MIC002-EI-INTR-RATE  PIC 9V9(5).
                         13  MIC002-EI-INTR-FREE-MOS  PIC 9(02).
                         13  MIC002-EI-FIRST-PAY-AMT  PIC 9(10)V99.
                         13  MIC002-EI-LAST-PAY-AMT  PIC 9(10)V99.
                         13  MIC002-EI-MON-INSTL-AMT  PIC 9(10)V99.
                         13  MIC002-EI-TOTAL-INSTL-AMT  PIC 9(10)V99.
                         13  MIC002-EI-OUTS-PRINCIPAL  PIC 9(10)V99.
                         13  MIC002-EI-OUTS-INTEREST  PIC 9(10)V99.
                         13  MIC002-EI-HANDLING-FEE  PIC 9(10)V99.
                         13  MIC002-EI-PLAN-TYPE  PIC X(01).
                         13  MIC002-EI-PROMOTION-FLAG  PIC X(01).
                         13  MIC002-EI-WAIVE-FR-MOS  PIC 9(02).
                         13  MIC002-EI-WAIVE-TO-MOS  PIC 9(02).
                         13  MIC002-EI-PLAN-ORG  PIC 9(03).
                         13  MIC002-EI-DBA-NAME  PIC X(25).
                         13  MIC002-ECOM-TRXN-CURR-EXPN  PIC 9(01).
                         13  MIC002-ECOM-IPM-DATA-CODE  PIC X(12).
                         13  FILLER              PIC X(854).
      * DE60 RESPONSE - MTIM - MIC002-MTIM-INQ-REC
                       11  ML60-MTIM REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-IM-PYMT-APP-INST-ID  PIC X(48).
                         13  MIC002-IM-DEVICE-NAME  PIC X(64).
                         13  MIC002-IM-CURR-STS-CDE  PIC X(01).
                         13  MIC002-IM-CURR-STS-DTE  PIC X(25).
                         13  MIC002-IM-PROV-STS-CDE  PIC X(01).
                         13  MIC002-IM-PROV-STS-DTE  PIC X(25).
                         13  MIC002-IM-TKN-REQ-NAME  PIC X(100).
                         13  MIC002-IM-PAN-SRC   PIC X(64).
                         13  FILLER              PIC X(372).
                         13  FILLER              PIC X(299).
      * DE60 RESPONSE - MTKP - MIC002-MTKP-INQ-REC
                       11  ML60-MTKP REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-MTKP-DATA    PIC X(700).
                         13  FILLER              PIC X(299).
      * DE60 RESPONSE - MTKQ - MIC002-MTKQ-INQ-REC
                       11  ML60-MTKQ REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-TQ-SCHME     PIC X(01).
                         13  MIC002-TQ-TOKEN     PIC X(19).
                         13  MIC002-TQ-DEVICE-IDX  PIC X(02).
                         13  MIC002-TQ-DATE-CHANGE  PIC 9(08).
                         13  MIC002-TQ-TIME-CHANGE  PIC 9(06).
                         13  MIC002-TQ-ASSURANCE-LEVEL  PIC X(02).
                         13  MIC002-TQ-REQUESTOR-ID  PIC X(11).
                         13  MIC002-TQ-STATUS    PIC X(01).
                         13  MIC002-TQ-ACTION-DATE  PIC 9(08).
                         13  MIC002-TQ-EXPIRY-DATE  PIC 9(04).
                         13  MIC002-TQ-PYMT-ACCT-REF  PIC X(29).
                         13  MIC002-TQ-FILLER    PIC X(109).
                         13  MIC002-TQ-NTWK-TOKEN  PIC X(500).
                         13  FILLER              PIC X(299).
      * DE60 RESPONSE - SAIQ - MIC002-SAIQ-LIST-INQ-REC
                       11  ML60-SAIQ REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-SAIQ-CR-STATUS  PIC X(01).
                         13  MIC002-SAIQ-B-SCORE  PIC 9(05).
                         13  MIC002-SAIQ-B-SCORE-IND  PIC X(01).
                         13  MIC002-SAIQ-CRLIMIT-PERM  PIC 9(09).
                         13  MIC002-SAIQ-CRLIMIT-TEMP  PIC 9(09).
                         13  MIC002-SAIQ-CRLM-TEMP-EFF-DTE  PIC 9(08).
                         13  MIC002-SAIQ-CRLM-TEMP-EXP-DTE  PIC 9(08).
                         13  MIC002-SAIQ-CM-ORG-NMBR  PIC 9(03).
                         13  MIC002-SAIQ-CM-TYPE  PIC 9(03).
                         13  MIC002-SAIQ-CM-CARD-NMBR  PIC 9(16).
                         13  MIC002-SAIQ-CM-DTE-OPENED  PIC 9(08).
                         13  MIC002-SAIQ-CM-STATUS  PIC X(01).
                         13  MIC002-SAIQ-CM-CYCLE  PIC 9(02).
                         13  MIC002-SAIQ-CM-USER-CODE  PIC X(02).
                         13  MIC002-SAIQ-CM-USER-CODE-2  PIC X(02).
                         13  MIC002-SAIQ-CM-USER-CODE-3  PIC X(02).
                         13  MIC002-SAIQ-CM-USER-CODE-4  PIC X(02).
                         13  MIC002-SAIQ-CM-USER-CODE-5  PIC X(02).
                         13  MIC002-SAIQ-CM-USER-CODE-6  PIC X(02).
                         13  MIC002-SAIQ-CM-BLOCK-CODE  PIC X(01).
                         13  MIC002-SAIQ-CM-DTE-BLOCK-CODE  PIC 9(08).
                         13  MIC002-SAIQ-CM-ALT-BLOCK-CODE  PIC X(01).
                         13  MIC002-SAIQ-CM-DTE-ALT-BLK-CD  PIC 9(08).
                         13  MIC002-SAIQ-CM-CRLIMIT  PIC 9(09).
                         13  MIC002-SAIQ-CM-CRLIMIT-IND  PIC X(01).
                         13  MIC002-SAIQ-CURR-BALANCE  PIC 9(09)V99.
                         13  MIC002-SAIQ-CURR-BALANCE-IND  PIC X(01).
                         13  MIC002-SAIQ-CASH-BALANCE  PIC 9(09)V99.
                         13  MIC002-SAIQ-CASH-BALANCE-IND  PIC X(01).
                         13  MIC002-SAIQ-RTL-BALANCE  PIC 9(09)V99.
                         13  MIC002-SAIQ-RTL-BALANCE-IND  PIC X(01).
                         13  MIC002-SAIQ-HI-BALANCE  PIC 9(09).
                         13  MIC002-SAIQ-HI-BALANCE-IND  PIC X(01).
                         13  MIC002-SAIQ-CM-NPL-IND  PIC X(01).
                         13  MIC002-SAIQ-CM-DELQ-HIST  PIC X(01).
                         13  MIC002-SAIQ-LAST-1ST-MTH-PYMT
                                 PIC 9(09)V99.
                         13  MIC002-SAIQ-LAST-1ST-MTH-IND  PIC X(01).
                         13  MIC002-SAIQ-LAST-2ND-MTH-PYMT
                                 PIC 9(09)V99.
                         13  MIC002-SAIQ-LAST-2ND-MTH-IND  PIC X(01).
                         13  MIC002-SAIQ-LAST-3RD-MTH-PYMT
                                 PIC 9(09)V99.
                         13  MIC002-SAIQ-LAST-3RD-MTH-IND  PIC X(01).
                         13  MIC002-SAIQ-LAST-4TH-MTH-PYMT
                                 PIC 9(09)V99.
                         13  MIC002-SAIQ-LAST-4TH-MTH-IND  PIC X(01).
                         13  MIC002-SAIQ-LAST-5TH-MTH-PYMT
                                 PIC 9(09)V99.
                         13  MIC002-SAIQ-LAST-5TH-MTH-IND  PIC X(01).
                         13  MIC002-SAIQ-LAST-6TH-MTH-PYMT
                                 PIC 9(09)V99.
                         13  MIC002-SAIQ-LAST-6TH-MTH-IND  PIC X(01).
                         13  MIC002-SAIQ-LAST-1ST-CYC-BAL  PIC 9(09)V99.
                         13  MIC002-SAIQ-LAST-1ST-CYC-IND  PIC X(01).
                         13  MIC002-SAIQ-LAST-2ND-CYC-BAL  PIC 9(09)V99.
                         13  MIC002-SAIQ-LAST-2ND-CYC-IND  PIC X(01).
                         13  MIC002-SAIQ-LAST-3RD-CYC-BAL  PIC 9(09)V99.
                         13  MIC002-SAIQ-LAST-3RD-CYC-IND  PIC X(01).
                         13  MIC002-SAIQ-LAST-4TH-CYC-BAL  PIC 9(09)V99.
                         13  MIC002-SAIQ-LAST-4TH-CYC-IND  PIC X(01).
                         13  MIC002-SAIQ-LAST-5TH-CYC-BAL  PIC 9(09)V99.
                         13  MIC002-SAIQ-LAST-5TH-CYC-IND  PIC X(01).
                         13  MIC002-SAIQ-LAST-6TH-CYC-BAL  PIC 9(09)V99.
                         13  MIC002-SAIQ-LAST-6TH-CYC-IND  PIC X(01).
                         13  MIC002-SAIQ-PLT-ORG-NMBR  PIC 9(03).
                         13  MIC002-SAIQ-PLT-TYPE-NMBR  PIC 9(03).
                         13  MIC002-SAIQ-PLT-CARD-NMBR  PIC X(19).
                         13  MIC002-SAIQ-PLT-EMBOSSER-NAME1  PIC X(26).
                         13  MIC002-SAIQ-PLT-RELATIONSHIP  PIC X(01).
                         13  MIC002-SAIQ-PLT-STATUS  PIC X(01).
                         13  MIC002-SAIQ-PLT-BLOCK-CODE  PIC X(01).
                         13  MIC002-SAIQ-PLT-EXP-DTE  PIC 9(04).
                         13  MIC002-SAIQ-PLT-TFT-DTE  PIC 9(08).
                         13  MIC002-SAIQ-PLT-ACT-CODE  PIC X(01).
                         13  MIC002-SAIQ-PLT-NEW-PLT-NBR  PIC X(19).
                         13  MIC002-SAIQ-PLT-NEW-PLT-EXP  PIC 9(04).
                         13  MIC002-SAIQ-PLT-PA  PIC 9(01).
                         13  MIC002-SAIQ-PLT-ISS-DTE  PIC 9(08).
                         13  MIC002-SAIQ-PLT-LAST-EXP-DTE  PIC 9(04).
                         13  MIC002-SAIQ-CR-CLT-CRLIMIT  PIC 9(11).
                         13  MIC002-SAIQ-CR-CLT-CRAVL  PIC 9(09)V99.
                         13  MIC002-SAIQ-CR-AVAIL-CREDIT  PIC 9(09)V99.
                         13  MIC002-SAIQ-CR-TEMP-LIMIT  PIC 9(11).
                         13  MIC002-SAIQ-CR-OVERPAY  PIC 9(09)V99.
                         13  MIC002-SAIQ-CM-CLT-CRLIMIT  PIC 9(11).
                         13  MIC002-SAIQ-CM-CLT-CRAVL  PIC 9(09)V99.
                         13  MIC002-SAIQ-CM-AVAIL-CREDIT  PIC 9(09)V99.
                         13  MIC002-SAIQ-CM-TEMP-LIMIT  PIC 9(11).
                         13  MIC002-SAIQ-CM-OVERPAY  PIC 9(09)V99.
                         13  MIC002-SAIQ-CM-CPP-IND  PIC X(01).
                         13  MIC002-SAIQ-CM-CPP-EFF-DTE  PIC 9(08).
                         13  MIC002-SAIQ-TC-USER-LIMIT-6  PIC 9(09)V99.
                         13  MIC002-SAIQ-RTL1-BALANCE  PIC 9(09)V99.
                         13  FILLER              PIC X(449).
      * DE60 RESPONSE - SCIQ - MIC002-SCIQ-LIST-INQ-REC
                       11  ML60-SCIQ REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-SCIQ-SHORT-NAME  PIC X(15).
                         13  MIC002-SCIQ-NAME-1  PIC X(30).
                         13  MIC002-SCIQ-NAME-2  PIC X(30).
                         13  MIC002-SCIQ-ADDR-1  PIC X(30).
                         13  MIC002-SCIQ-ADDR-2  PIC X(30).
                         13  MIC002-SCIQ-CITY    PIC X(28).
                         13  MIC002-SCIQ-ZIP-CODE  PIC X(09).
                         13  MIC002-SCIQ-HOME-PHONE  PIC X(18).
                         13  MIC002-SCIQ-HANDPHONE  PIC X(18).
                         13  MIC002-SCIQ-EMAIL-ADDR  PIC X(50).
                         13  MIC002-SCIQ-EU-MARITAL-STATUS  PIC 9(01).
                         13  MIC002-SCIQ-EU-SEX  PIC 9(01).
                         13  MIC002-SCIQ-EU-TYPE-OF-RES  PIC X(02).
                         13  MIC002-SCIQ-STATE   PIC X(02).
                         13  MIC002-SCIQ-SECURITY-QN  PIC X(30).
                         13  MIC002-SCIQ-EU-LEZ-CODE  PIC X(04).
                         13  MIC002-SCIQ-SMSA    PIC 9(04).
                         13  MIC002-SCIQ-CENSUS-TRACT  PIC 9(07).
                         13  MIC002-SCIQ-DTE-BIRTH  PIC 9(08).
                         13  MIC002-SCIQ-INCOME  PIC 9(09).
                         13  MIC002-SCIQ-OFF-PHONE-FLAG  PIC X(01).
                         13  MIC002-SCIQ-CO-TAX-ID-TYPE  PIC X(01).
                         13  MIC002-SCIQ-FOREIGN-CNTY-IND  PIC X(01).
                         13  MIC002-SCIQ-VVIP-FLAG  PIC X(01).
                         13  MIC002-SCIQ-CR-STATUS  PIC X(01).
                         13  MIC002-SCIQ-ADDNAME-FLAG  PIC X(01).
                         13  MIC002-SCIQ-ADDR-3  PIC X(30).
                         13  MIC002-SCIQ-PLT-ORG-NMBR  PIC 9(03).
                         13  MIC002-SCIQ-PLT-TYPE-NMBR  PIC 9(03).
                         13  MIC002-SCIQ-PLT-CARD-NMBR  PIC X(19).
                         13  MIC002-SCIQ-PLT-EMBOSSER-NAME1  PIC X(26).
                         13  MIC002-SCIQ-PLT-RELATIONSHIP  PIC X(01).
                         13  MIC002-SCIQ-PLT-STATUS  PIC X(01).
                         13  MIC002-SCIQ-PLT-BLOCK-CODE  PIC X(01).
                         13  MIC002-SCIQ-PLT-DETAILS-1V  PIC X(54).
                         13  MIC002-SCIQ-PLT-OPT-IND-1V  PIC X(01).
                         13  MIC002-SCIQ-PLT-ABC-IND-1V  PIC X(01).
                         13  FILLER              PIC X(527).
      * DE60 RESPONSE - SICR - MIC002-SICR-RESP-INFO-REC
                       11  ML60-SICR REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-SICR-CR-NAME-1  PIC X(30).
                         13  MIC002-SICR-CR-ADDR-1  PIC X(30).
                         13  MIC002-SICR-CR-ADDR-2  PIC X(30).
                         13  MIC002-SICR-CR-ZIP-CODE  PIC X(09).
                         13  FILLER              PIC X(900).
      * DE60 RESPONSE - SMIK - MIC002-SMIK-LIST-INQ-REC
                       11  ML60-SMIK REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-SMIK-TNG-CARD-NMBR  PIC 9(16).
                         13  MIC002-SMIK-TNG-ZNG-IND  PIC X(01).
                         13  MIC002-SMIK-TNG-RELOAD-OPT  PIC X(01).
                         13  MIC002-SMIK-TNG-MFG-NMBR  PIC 9(16).
                         13  MIC002-SMIK-TNG-MFG-RCV-DATE  PIC 9(06).
                         13  MIC002-SMIK-TNG-CARD-STATUS  PIC X(01).
                         13  MIC002-SMIK-TNG-REN-MFG-NMBR  PIC 9(16).
                         13  MIC002-SMIK-TNG-REN-MFG-RCV-DT  PIC 9(06).
                         13  MIC002-SMIK-TNG-REN-MFG-EXP-DT  PIC 9(06).
                         13  MIC002-SMIK-TNG-REN-MFG-STATUS  PIC X(01).
                         13  MIC002-SMIK-TNG-OLD-MFG-NMBR  PIC 9(16).
                         13  MIC002-SMIK-TNG-OLD-MFG-RCV-DT  PIC 9(06).
                         13  MIC002-SMIK-TNG-OLD-MFG-EXP-DT  PIC 9(06).
                         13  FILLER              PIC X(901).
      * DE60 RESPONSE - SPTE - MIC002-SPTE-RESP-INFO-REC
                       11  ML60-SPTE REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-TE-FIRST-INSTL-AMT  PIC 9(10)V99.
                         13  MIC002-TE-FIRST-PYMT-DATE  PIC 9(08).
                         13  MIC002-TE-MONTHLY-INSTL-AMT  PIC 9(10)V99.
                         13  MIC002-TE-LAST-INSTL-AMT  PIC 9(10)V99.
                         13  MIC002-TE-LAST-PYMT-DATE  PIC 9(08).
                         13  MIC002-TE-OUTSTD-PRINCIPAL  PIC 9(10)V99.
                         13  MIC002-TE-OUTSTD-UNEARN-INT  PIC 9(10)V99.
                         13  MIC002-TE-IPP-DATE  PIC 9(08).
                         13  MIC002-TE-IPP-TIME  PIC 9(07).
                         13  FILLER              PIC X(908).
      * DE60 RESPONSE - VCIH - MIC002-VCIH-STATEMENT-INQ-REC
                       11  ML60-VCIH REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-VCIH-DATA-LEN060  PIC 9(03).
                         13  MIC002-VCIH-CR-EXT-ACT-NBR  PIC X(30).
                         13  MIC002-VCIH-FEE-BASED-SALES  PIC S9(09)V99.
                         13  MIC002-VCIH-AVG-TICKET  PIC S9(07)V99.
                         13  MIC002-VCIH-TTL-FEES  PIC S9(07)V99.
                         13  MIC002-VCIH-TTL-DISC  PIC S9(07)V99.
                         13  MIC002-VCIH-EFF-RATE  PIC 9V9(05).
                         13  MIC002-VCIH-DBA-NME  PIC X(25).
                         13  MIC002-VCIH-DISC-FREQ  PIC 9(02).
                         13  MIC002-VCIH-AMT-DISC-GST  PIC S9(7)V99.
                         13  MIC002-VCIH-AMT-FEES-GST  PIC S9(7)V99.
                         13  FILLER              PIC X(877).
      * DE60 RESPONSE - VLIC - MIC002-VLIC-CHBK-TXN-INQ
                       11  ML60-VLIC REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-VLIC-DATA-LEN060  PIC 9(03).
                         13  MIC002-VLIC-TXN-ARN  PIC X(23).
                         13  MIC002-VLIC-TXN-CDE  PIC 9(04).
                         13  MIC002-VLIC-APPR-CDE  PIC X(06).
                         13  MIC002-VLIC-TXN-AMT  PIC 9(10)V99.
                         13  MIC002-VLIC-TXN-CCY  PIC 9(03).
                         13  MIC002-VLIC-BIL-AMT  PIC 9(10)V99.
                         13  MIC002-VLIC-BIL-CCY  PIC 9(03).
                         13  MIC002-VLIC-STTL-AMT  PIC 9(10)V99.
                         13  MIC002-VLIC-STTL-CCY  PIC X(03).
                         13  MIC002-VLIC-POS-MODE  PIC X(02).
                         13  MIC002-VLIC-MCC     PIC X(04).
                         13  MIC002-VLIC-MERCH-NME  PIC X(30).
                         13  MIC002-VLIC-MERCH-ID  PIC X(15).
                         13  MIC002-VLIC-EC-SEC-LEVEL  PIC X(03).
                         13  MIC002-VLIC-EC-IND  PIC X(01).
                         13  MIC002-VLIC-VROL-FIN-ID  PIC X(11).
                         13  MIC002-VLIC-VROL-CASE-NO  PIC X(10).
                         13  MIC002-VLIC-TERM-ID  PIC X(15).
                         13  MIC002-VLIC-TXN-DATE  PIC X(08).
                         13  MIC002-VLIC-TXN-TYPE  PIC X(02).
                         13  MIC002-VLIC-CHBK-RSN-CDE  PIC X(04).
                         13  MIC002-VLIC-ISS-REF-ID  PIC X(10).
                         13  MIC002-VLIC-POS-DATA-CDE  PIC X(12).
                         13  FILLER              PIC X(791).
      * DE60 RESPONSE - VLLC - MIC002-VLLC-CHBK-TXN-LIST
                       11  ML60-VLLC REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-VLLC-RESP-LEN060  PIC 9(03).
                         13  MIC002-VLLC-TXN-ORG  PIC 9(03).
                         13  MIC002-VLLC-ARN     PIC X(23).
                         13  MIC002-VLLC-ISS-INST-ID  PIC X(11).
                         13  MIC002-VLLC-ACQ-INST-ID  PIC X(11).
                         13  MIC002-VLLC-TXN-CDE  PIC X(04).
                         13  MIC002-VLLC-REV-IND  PIC X(01).
                         13  MIC002-VLLC-PROC-DTE  PIC 9(08).
                         13  MIC002-VLLC-TXN-AMT  PIC 9(10)V99.
                         13  MIC002-VLLC-TXN-CCY  PIC X(03).
                         13  MIC002-VLLC-NETW-IND  PIC X(01).
                         13  MIC002-VLLC-TXN-DIR  PIC X(01).
                         13  MIC002-VLLC-STATUS  PIC X(01).
                         13  MIC002-VLLC-UPD-OPER-ID  PIC X(20).
                         13  MIC002-VLLC-HIST-KEY  PIC X(16).
                         13  MIC002-VLLC-FIL-IDX  PIC 9(02).
                         13  FILLER              PIC X(879).
      * DE60 RESPONSE - VMDR - MIC002-VMDR-MDR-INQ-REC
                       11  ML60-VMDR REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-VMDR-RESP-LEN060  PIC 9(03).
                         13  MIC002-VMDR-PROG-OFFER-ID  PIC X(06).
                         13  MIC002-VMDR-ID      PIC X(06).
                         13  MIC002-VMDR-SCHEME  PIC X(01).
                         13  MIC002-VMDR-DISC    PIC X(20).
                         13  MIC002-VMDR-RESP-LEN061  PIC 9(03).
                         13  MIC002-VMDR-DISC-PLAN  PIC X(06).
                         13  MIC002-VMDR-DISC-PLAN-DESC  PIC X(30).
                         13  MIC002-VMDR-T1-LOWER-LMT  PIC 9(10)V99.
                         13  MIC002-VMDR-T1-ITL-RTE  PIC 9(2)V9(05).
                         13  MIC002-VMDR-T1-ITL-FLT  PIC 9(10)V99.
                         13  MIC002-VMDR-T1-DOM-RTE  PIC 9(2)V9(05).
                         13  MIC002-VMDR-T1-DOM-FLT  PIC 9(10)V99.
                         13  MIC002-VMDR-T1-OUS-RTE  PIC 9(2)V9(05).
                         13  MIC002-VMDR-T1-OUS-FLT  PIC 9(10)V99.
                         13  FILLER              PIC X(855).
      * DE60 RESPONSE - VMI1 - MIC002-VMI1-RESP-INFO-REC
                       11  ML60-VMI1 REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-VMI1-RESP-LEN060  PIC 9(03).
                         13  MIC002-VMI1-AMT060  PIC 9(13)V99.
                         13  MIC002-VMI1-AMT060-IND  PIC X(01).
                         13  MIC002-VMI1-INTR-RATE060  PIC 9(03)V99.
                         13  MIC002-VMI1-INT060  PIC 9(13)V99.
                         13  MIC002-VMI1-INT060-IND  PIC X(01).
                         13  MIC002-VMI1-TENURE-060  PIC 9(03)V99.
                         13  MIC002-VMI1-PRIN-INT060  PIC 9(13)V99.
                         13  MIC002-VMI1-PRIN-INT060-IND  PIC X(01).
                         13  MIC002-VMI1-FIRST-INS060  PIC 9(13)V99.
                         13  MIC002-VMI1-FIRST-INS060-IND  PIC X(01).
                         13  MIC002-VMI1-MONTH-INS060  PIC 9(13)V99.
                         13  MIC002-VMI1-MONTH-INS060-IND  PIC X(01).
                         13  MIC002-VMI1-LAST-INS060  PIC 9(13)V99.
                         13  MIC002-VMI1-LAST-INS060-IND  PIC X(01).
                         13  MIC002-VMI1-EFF-INTR-RATE060  PIC 9(03)V99.
                         13  MIC002-VMI1-RESP-LEN061  PIC 9(03).
                         13  MIC002-VMI1-TENURE-061  PIC 9(03).
                         13  MIC002-VMI1-CYCLE-DATE061  PIC 9(08).
                         13  MIC002-VMI1-AMT061  PIC 9(13)V99.
                         13  MIC002-VMI1-AMT061-IND  PIC X(01).
                         13  MIC002-VMI1-INTR-EARN061  PIC 9(13)V99.
                         13  MIC002-VMI1-INTR-EARN061-IND  PIC X(01).
                         13  MIC002-VMI1-INTR-UNBIL061  PIC 9(13)V99.
                         13  MIC002-VMI1-INTR-UNBIL061-IND  PIC X(01).
                         13  MIC002-VMI1-PRIN-AMT061  PIC 9(13)V99.
                         13  MIC002-VMI1-PRIN-AMT061-IND  PIC X(01).
                         13  MIC002-VMI1-RESP-LEN062  PIC 9(03).
                         13  MIC002-VMI1-TENURE-062  PIC 9(03).
                         13  MIC002-VMI1-CYCLE-DATE062  PIC 9(08).
                         13  MIC002-VMI1-AMT062  PIC 9(13)V99.
                         13  MIC002-VMI1-AMT062-IND  PIC X(01).
                         13  MIC002-VMI1-INTR-EARN062  PIC 9(13)V99.
                         13  MIC002-VMI1-INTR-EARN062-IND  PIC X(01).
                         13  MIC002-VMI1-INTR-UNBIL062  PIC 9(13)V99.
                         13  MIC002-VMI1-INTR-UNBIL062-IND  PIC X(01).
                         13  MIC002-VMI1-PRIN-AMT062  PIC 9(13)V99.
                         13  MIC002-VMI1-PRIN-AMT062-IND  PIC X(01).
                         13  MIC002-VMI1-RESP-LEN063  PIC 9(03).
                         13  MIC002-VMI1-TENURE-063  PIC 9(03).
                         13  MIC002-VMI1-CYCLE-DATE063  PIC 9(08).
                         13  MIC002-VMI1-AMT063  PIC 9(13)V99.
                         13  MIC002-VMI1-AMT063-IND  PIC X(01).
                         13  MIC002-VMI1-INTR-EARN063  PIC 9(13)V99.
                         13  MIC002-VMI1-INTR-EARN063-IND  PIC X(01).
                         13  MIC002-VMI1-INTR-UNBIL063  PIC 9(13)V99.
                         13  MIC002-VMI1-INTR-UNBIL063-IND  PIC X(01).
                         13  MIC002-VMI1-PRIN-AMT063  PIC 9(13)V99.
                         13  MIC002-VMI1-PRIN-AMT063-IND  PIC X(01).
                         13  MIC002-VMI1-RESP-LEN116  PIC 9(03).
                         13  MIC002-VMI1-TENURE-116  PIC 9(03).
                         13  MIC002-VMI1-CYCLE-DATE116  PIC 9(08).
                         13  MIC002-VMI1-AMT116  PIC 9(13)V99.
                         13  MIC002-VMI1-AMT116-IND  PIC X(01).
                         13  MIC002-VMI1-INTR-EARN116  PIC 9(13)V99.
                         13  MIC002-VMI1-INTR-EARN116-IND  PIC X(01).
                         13  MIC002-VMI1-INTR-UNBIL116  PIC 9(13)V99.
                         13  MIC002-VMI1-INTR-UNBIL116-IND  PIC X(01).
                         13  MIC002-VMI1-PRIN-AMT116  PIC 9(13)V99.
                         13  MIC002-VMI1-PRIN-AMT116-IND  PIC X(01).
                         13  MIC002-VMI1-RESP-LEN117  PIC 9(03).
                         13  MIC002-VMI1-TENURE-117  PIC 9(03).
                         13  MIC002-VMI1-CYCLE-DATE117  PIC 9(08).
                         13  MIC002-VMI1-AMT117  PIC 9(13)V99.
                         13  MIC002-VMI1-AMT117-IND  PIC X(01).
                         13  MIC002-VMI1-INTR-EARN117  PIC 9(13)V99.
                         13  MIC002-VMI1-INTR-EARN117-IND  PIC X(01).
                         13  MIC002-VMI1-INTR-UNBIL117  PIC 9(13)V99.
                         13  MIC002-VMI1-INTR-UNBIL117-IND  PIC X(01).
                         13  MIC002-VMI1-PRIN-AMT117  PIC 9(13)V99.
                         13  MIC002-VMI1-PRIN-AMT117-IND  PIC X(01).
                         13  FILLER              PIC X(495).
      * DE60 RESPONSE - VMIC - MIC002-VMIC-CONTACT-INQ-REC
                       11  ML60-VMIC REDEFINES
                               MIC003-B060-OUTPUT-DATA-1.
                         13  MIC002-VMIC-DATA-LEN060  PIC 9(03).
                         13  MIC002-VMIC-STATUS  PIC X(01).
                         13  MIC002-VMIC-OWN-ID  PIC X(01).
                         13  MIC002-VMIC-PSL-IDN  PIC X(30).
                         13  MIC002-VMIC-PSL-NME-1  PIC X(30).
                         13  MIC002-VMIC-PSL-NME-2  PIC X(30).
                         13  MIC002-VMIC-ADR-1   PIC X(30).
                         13  MIC002-VMIC-ADR-2   PIC X(30).
                         13  MIC002-VMIC-ADR-3   PIC X(30).
                         13  MIC002-VMIC-ADR-4   PIC X(30).
                         13  MIC002-VMIC-STE     PIC X(02).
                         13  MIC002-VMIC-CTY     PIC X(13).
                         13  MIC002-VMIC-CRY     PIC X(03).
                         13  MIC002-VMIC-HOME-CRY  PIC X(03).
                         13  MIC002-VMIC-PST-CDE  PIC X(10).
                         13  MIC002-VMIC-TEL-1   PIC X(30).
                         13  MIC002-VMIC-TEL-2   PIC X(30).
                         13  MIC002-VMIC-TEL-3   PIC X(30).
                         13  MIC002-VMIC-FAX     PIC X(30).
                         13  MIC002-VMIC-EML     PIC X(66).
                         13  MIC002-VMIC-MMO     PIC X(66).
                         13  MIC002-VMIC-MER-REG-NME  PIC X(30).
                         13  FILLER              PIC X(471).
                       11  MIC003-B061-OUTPUT-DATA-2-LEN PIC S9(03)
                               COMP-3.
                       11  MIC003-B061-OUTPUT-DATA-2 PIC X(999).
                       11  FILLER REDEFINES MIC003-B061-OUTPUT-DATA-2.
                         13  MIC003-B061-CCTH-OUT PIC X(124) OCCURS 8
                                 TIMES.
                         13  FILLER PIC X(07).
                       11  MIC003-B061-CCAA-DATA REDEFINES
                               MIC003-B061-OUTPUT-DATA-2.
                         13  MIC003-B061-CCAA-ID-ISS-CTRY PIC X(02).
                         13  MIC003-B061-CCAA-ID-EXP-DTE PIC 9(08).
                         13  MIC003-B061-CCAA-ALT-ID-TYP PIC 9(03).
                         13  MIC003-B061-ALT-ID-ISS-CTRY PIC X(02).
                         13  MIC003-B061-ALT-ID-EXP-DTE PIC 9(08).
                         13  MIC003-B061-FOREIGN-TAX-ID PIC X(20).
                         13  MIC003-B061-FOREIGN-TAX-IS-CTY PIC X(02).
                         13  MIC003-B061-REGIONAL-IND PIC X(01).
                         13  MIC003-B061-VISA-TYP PIC X(03).
                         13  MIC003-B061-VISA-DOC-NO PIC X(40).
                         13  MIC003-B061-VISA-EXP-DTE PIC 9(08).
                         13  MIC003-B061-PEP-IND PIC X(01).
                         13  MIC003-B061-PEP-CLASSIFICATION PIC X(02).
                         13  MIC003-B061-PEP-RELATIONSHIP PIC X(03).
                         13  MIC003-B061-PEP-TEXT-OTHERS PIC X(50).
                         13  MIC003-B061-CITIZEN PIC X(01).
                         13  MIC003-B061-EMER-CONTACT PIC X(12).
                         13  MIC003-B061-CUSTOMER-NAME PIC X(200).
                         13  FILLER PIC X(633).
                       11  MIC003-B062-OUTPUT-DATA-3-LEN PIC S9(03)
                               COMP-3.
                       11  MIC003-B062-OUTPUT-DATA-3 PIC X(999).
                       11  MIC003-B062-RED REDEFINES
                               MIC003-B062-OUTPUT-DATA-3.
                         13  MIC003-B062-TXN-IDENTIFIER PIC 9(15).
                         13  MIC003-B062-CARD-LEVEL PIC X(02).
                         13  MIC003-B062-PAN-LAST-4 PIC X(04).
                         13  MIC003-B062-ASSR-LVL PIC X(02).
                         13  MIC003-B062-TOKEN PIC X(19).
                         13  MIC003-B062-REQ-ID PIC 9(11).
                         13  MIC003-B062-PYMT-ACCT-REF PIC X(29).
                         13  MIC003-B062-ORIG-TRANS-AMOUNT PIC
                                 S9(10)V99 COMP-3.
                         13  MIC003-B062-AUTH-SRC-CODE PIC X(01).
                         13  MIC003-B062-TOKEN-RESP-INFO PIC X(01).
                         13  MIC003-B062-NTWK-RESP-CODE PIC X(02).
                         13  MIC003-B062-MAIL-PHONE-IND PIC 9(02).
                         13  MIC003-B062-CRD-ID-METH PIC X(01).
                         13  MIC003-B062-AUTH-CHAR-IND PIC X(01).
                         13  MIC003-B062-VLDTN-CODE PIC X(04).
                         13  MIC003-B062-SPEND-QUAL-IND PIC X(01).
                         13  MIC003-B062-ACCT-FUND-SRC PIC X(01).
                         13  MIC003-B062-APPL-SPCL-SVC PIC X(01).
                         13  FILLER PIC X(895).
                       11  FILLER REDEFINES MIC003-B062-OUTPUT-DATA-3.
                         13  MIC003-B062-CCTH-OUT PIC X(124) OCCURS 8
                                 TIMES.
                         13  FILLER PIC X(07).
                       11  MIC003-B063-OUTPUT-DATA-4-LEN PIC S9(03)
                               COMP-3.
                       11  MIC003-B063-OUTPUT-DATA-4 PIC X(999).
                       11  MIC003-B063-RED REDEFINES
                               MIC003-B063-OUTPUT-DATA-4.
                         13  MIC003-B063-BNKNT-DATE PIC X(04).
                         13  MIC003-B063-BNKNT-DATA.
                           15  MIC003-B063-FNCL-NTWK-CDE PIC X(03).
                           15  MIC003-B063-BNKNT-REF-NBR PIC X(09).
                         13  MIC003-B063-TXN-LINK-ID PIC X(22).
                         13  FILLER PIC X(961).
                       11  FILLER REDEFINES MIC003-B063-OUTPUT-DATA-4.
                         13  MIC003-B063-CCTH-OUT PIC X(124) OCCURS 8
                                 TIMES.
                         13  FILLER PIC X(07).
                       11  MIC003-B116-OUTPUT-DATA-5-LEN PIC S9(03)
                               COMP-3.
                       11  MIC003-B116-OUTPUT-DATA-5 PIC X(999).
                       11  FILLER REDEFINES MIC003-B116-OUTPUT-DATA-5.
                         13  MIC003-B116-CCTH-OUT PIC X(124) OCCURS 8
                                 TIMES.
                         13  FILLER PIC X(07).
                       11  MIC003-B117-OUTPUT-DATA-6-LEN PIC S9(03)
                               COMP-3.
                       11  MIC003-B117-OUTPUT-DATA-6 PIC X(999).
                       11  FILLER REDEFINES MIC003-B117-OUTPUT-DATA-6.
                         13  MIC003-B117-CCTH-OUT PIC X(124) OCCURS 8
                                 TIMES.
                         13  FILLER PIC X(07).
      *---------------------------------------------------------------*
      * LAYOUT 2 - SINGAPORE (MAX LRECL 8349)                         *
      * SG MIC003 BODY (QUEUE-REC X(7950)) NOT YET EXPANDED - SUPPLY  *
      * THE SG MIC003 COPYBOOK TO GENERATE THE DETAILED SG MAPS.      *
      *---------------------------------------------------------------*
       01  MILOG-ONL-RECORD-SG.
           03  MIC004-LOG-FILE-KEY-SG.
               05  MIC004-CARDHOLDER-NMBR-SG     PIC X(19).
               05  MIC004-ALT-KEY-SG.
                   07  MIC004-TRANS-DATE-SG      PIC S9(08)
                                                 COMP-3.
                   07  MIC004-TRANS-TIME-SG      PIC S9(06)
                                                 COMP-3.
                   07  MIC004-DELIVERY-CHNL-SG   PIC X(08).
                   07  MIC004-TRACE-NUMBER-SG    PIC S9(06)
                                                 COMP-3.
                   07  MIC004-SEQUENCE-NBR-SG    PIC S9(03)
                                                 COMP-3.
           03  MIC004-MTI-SG                     PIC S9(04)
                                                 COMP-3.
           03  MIC004-REC-TYPE-SG                PIC X(01).
           03  MIC004-DATE-STAMP-SG              PIC S9(08)
                                                 COMP-3.
           03  MIC004-TIME-STAMP-SG              PIC S9(06)
                                                 COMP-3.
           03  MIC004-REC-STATUS-SG              PIC X(01).
           03  MIC004-NETWK-POS-DATA-CD-SG       PIC X(12).
           03  MIC004-CARD-TYPE-SG               PIC X(01).
           03  MIC004-TXN-IC-SG                  PIC X(02).
           03  FILLER                            PIC X(97).
           03  MIC004-DATA-AREA-SG               PIC X(8181).
      * ---- TYPE A/B: DATA AREA = MIC003 QUEUE RECORD (SG) ----
           03  MIC004-MIC003-REC-SG REDEFINES
               MIC004-DATA-AREA-SG.
               05  MIC003-DATE-RECEIVED-SG       PIC 9(08).
               05  MIC003-TIME-RECEIVED-SG       PIC 9(06).
               05  MIC003-TERMINAL-ID-SG         PIC X(04).
               05  MIC003-TRACE-IND-SG           PIC X(01).
               05  MIC003-SAVE-AREA-SG           PIC X(50).
               05  MIC003-CARD-TYPE-SG           PIC X(01).
               05  MIC003-IPM-DE22-POS-DC-SG     PIC X(12).
               05  MIC003-TXN-IC-SG              PIC X(02).
               05  MIC003-TCP-QUEUE-SG           PIC X(08).
               05  FILLER                        PIC X(07).
               05  MIC003-MESSAGE-TYPE-ID-SG     PIC 9(04).
               05  MIC003-BYTE-MAP-IND-REC-SG    PIC X(128).
               05  MIC003-QUEUE-REC-SG           PIC X(7950).

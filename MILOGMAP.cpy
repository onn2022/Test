      *---------------------------------------------------------------*
      * MILOGMAP - MILOG (CLKMLOG.DAT) RECORD LAYOUT WITH PER-        *
      * TRANSACTION FIELD MAPS FOR ALL MBI TRANSACTIONS - MY AND SG   *
      *---------------------------------------------------------------*
      * NOTE: THIS MAPS THE FIXED-8000 DAILY BATCH EXTRACT FILE       *
      * (CLKMLOG.DAT WRITTEN BY MIDXEIS) ONLY.  DO NOT USE IT ON THE  *
      * ONLINE MILOG1/2/3 VSAM FILES (xxxMBI.ONLVSM.*.MILOGn) - THOSE *
      * ARE VARIABLE LENGTH (252-8047 MY / 252-8349 SG) WITH A 42-    *
      * BYTE KEY AND COMP-3 PACKED DATE/TIME.  USE MILOGONL INSTEAD.  *
      *---------------------------------------------------------------*
      * BASE RECORD ...... CLKMLOG-RECORD (8000 BYTES, REF MILOGDAT)  *
      * REQUEST MAPS ..... ML48-<TXN> REDEFINES the DE48 additional-  *
      *                    data area (bytes 811-1809 of the record).  *
      *                    First 150 bytes = common MIC003 DE48       *
      *                    prefix (trans-code/service/terminal/       *
      *                    request-type/no-of-trxn/seq/name/dob/id/   *
      *                    phones/security-qn/reason/2nd-acct).       *
      * RESPONSE MAPS ... ML60-<TXN> REDEFINES output payload slot 1  *
      *                    (DE60/B060, bytes 1992-2990).  Payloads    *
      *                    spill into B061/B062/B063/B116/B117 in the *
      *                    same layout (+1002 bytes per slot).        *
      * MAINT/UPDATE TXNS HAVE NO OUTPUT PAYLOAD - RESULT IS DE39     *
      * ACTION CODE (BYTES 502-504) PLUS THE MIC004 ACTIVITY LOG.     *
      * REPEATING DETAIL BLOCKS ARE MAPPED AT THEIR FIRST OCCURRENCE. *
      * FIELD NAMES ARE KEPT FROM THE SOURCE MIC002/MIC003/PROGRAM    *
      * COPYBOOKS - QUALIFY DUPLICATES, E.G. FIELD OF ML60-CCPS.      *
      *---------------------------------------------------------------*
      * TRANSACTION DIRECTORY (REQ = ML48-x / RESP = ML60-x)          *
      *   CCPS      ML60  PREVIOUS STATEMENT ENQUIRY
      *   CCBP      ML60  BONUS-POINT REDEMPTION
      *   PYMT      ML60  CASH/CHEQUE PAYMENT
      *   AUTH      DE39  AUTHORIZATION FINANCIAL
      *   CASH      DE39  CASH ADVANCE
      *   RTL       DE39  RETAIL DEBIT
      *   ECOM      ML60  E-COMMERCE REQUEST
      *   ECOM-REV  DE39  E-COMMERCE REVERSAL
      *   CPVU      DE39  CONTACTLESS VALUE UPDATE
      *   CCAA      DE39  CUSTOMER ADDRESS/CONTACT MAINT
      *   CCMC      DE39  CUSTOMER ADDRESS/CONTACT MAINT
      *   CCCP      DE39  PERM CREDIT-LIMIT MAINT
      *   CCCT      DE39  TEMP CREDIT-LIMIT MAINT
      *   CCAV-IVR  DE39  CARD ACTIVATION (IVR)
      *   CCOP      DE39  SET PAYMENT METHOD
      *   CCFU      DE39  CARD-NOT-PRESENT FLAG UPDATE
      *   COFU      DE39  OVERSEAS FLAG UPDATE
      *   CPCG      DE39  CHIP&PIN PIN CHANGE
      *   PINC      DE39  PIN CHANGE
      *   CPRQ      DE39  PIN REQUEST
      *   CCRT      DE39  CARD REISSUE
      *   SCAP      DE39  SPECIAL CARD-ACCT PROC
      *   PRPP      DE39  DUITNOW REAL-TIME PAYMENT
      *   SP2P-1100 DE39  P2P TRANSFER
      *   GCVM      DE39  GET CVM/LIMIT
      *   MAAQ      DE39  OCTO ACCOUNT REQUEST
      *   MSIC      DE39  MERCHANT MSIC
      *   MTAM      DE39  OCTO ACCOUNT/CARD REQUEST
      *   MTIM      ML60  OCTO/RBK2 INTERFACE
      *   MTKA      DE39  TOKEN ACTIVATE
      *   MTKM      DE39  TOKEN MAINTENANCE
      *   MTKP      ML60  TOKEN PROVISION
      *   MTKQ      ML60  TOKEN INQUIRY
      *   NBPS      DE39  NBPS / NATIONAL PAYMENT
      *   SAIQ      ML60  SPECIAL ACCOUNT INQ
      *   SCIK      DE39  SPECIAL CARDHOLDER LIST
      *   SCIQ      ML60  SPECIAL CUSTOMER INQ
      *   SCTF      DE39  SPECIAL TRANSFER
      *   SICR      ML60  SPECIAL INQ RESP
      *   SMCS      DE39  SPECIAL MC-STMT
      *   SMIK      ML60  SPECIAL MULTI-INQ
      *   SPCD      DE39  SPECIAL CARD DATA
      *   SPPT      DE39  SPECIAL PAYMENT
      *   SPTD      DE39  SPECIAL PAYMENT DETAIL
      *   SPTE      ML60  SPECIAL PAYMENT ENTRY
      *   VCIC      DE39  VISA CUSTOMER INQUIRY
      *   VCIH      ML60  VISA STMT INQ
      *   VLIC      ML60  VISA CHARGEBACK INQ
      *   VLLC      ML60  VISA CHARGEBACK LIST
      *   VMDR      ML60  VISA MDR INQUIRY
      *   VMI1      ML60  VISA MI INQUIRY
      *   VMIC      ML60  VISA CONTACT INQUIRY
      *---------------------------------------------------------------*
       01  CLKMLOG-RECORD.
           03  CLKMLOG-KEY.
               05  CLKMLOG-CARDHOLDER-NMBR       PIC X(19).
               05  CLKMLOG-TRANSACTION-DATE      PIC 9(08).
               05  CLKMLOG-TRANSACTION-TIME      PIC 9(06).
               05  CLKMLOG-DELIVERY-CHANNEL      PIC X(08).
               05  CLKMLOG-TRACE-NUMBER          PIC 9(06).
               05  CLKMLOG-SEQUENCE-NUMBER       PIC 9(03).
           03  CLKMLOG-MTI                       PIC 9(04).
           03  CLKMLOG-REC-TYPE                  PIC X(01).
           03  CLKMLOG-DATE-STAMP                PIC 9(08).
           03  CLKMLOG-TIME-STAMP                PIC 9(06).
           03  CLKMLOG-REC-STATUS                PIC X(01).
           03  CLKMLOG-NETWK-POS-DATA-CODE       PIC X(12).
           03  CLKMLOG-CARD-TYPE                 PIC X(01).
           03  CLKMLOG-TXN-IC                    PIC X(02).
           03  FILLER                            PIC X(12).
           03  CLKMLOG-DATE-RECEIVED             PIC 9(08).
           03  CLKMLOG-TIME-RECEIVED             PIC 9(06).
           03  CLKMLOG-TERMINAL-ID               PIC X(04).
           03  CLKMLOG-TRACE-IND                 PIC X(01).
           03  CLKMLOG-SAVE-AREA                 PIC X(50).
           03  CLKMLOG-CARD-TYP                  PIC X(01).
           03  CLKMLOG-IPM-DE22-POS-DATA-CODE    PIC X(12).
           03  CLKMLOG-TRAN-IC                   PIC X(02).
           03  FILLER                            PIC X(15).
           03  CLKMLOG-MESSAGE-TYPE-ID           PIC 9(04).
           03  CLKMLOG-BYTE-MAP-IND-REC          PIC X(128).
           03  CLKMLOG-B002-PAN-LEN              PIC 9(02).
           03  CLKMLOG-B002-PAN-19               PIC X(19).
           03  CLKMLOG-B003-PROCESSING-CODE      PIC 9(06).
           03  CLKMLOG-B004-TRANS-AMOUNT         PIC 9(10).99.
           03  CLKMLOG-B011-SYS-AUDT-TRACE       PIC 9(07).
           03  CLKMLOG-B012-LCL-DATE-TIME        PIC 9(12).
           03  CLKMLOG-DATE-EFFECTIVE            PIC 9(04).
           03  CLKMLOG-DATE-EXPIRATION           PIC 9(04).
           03  CLKMLOG-DATE-CAPTUR               PIC 9(04).
           03  CLKMLOG-B022-POS-DATA-CODE        PIC X(12).
           03  CLKMLOG-B024-FUNCTION-CODE        PIC 9(03).
           03  CLKMLOG-B026-CARD-ACPTOR-BIZ      PIC 9(04).
           03  CLKMLOG-B030-AMOUNT-ORIG-TRANS    PIC 9(10).99.
           03  CLKMLOG-B030-AMOUNT-ORIG-RECON    PIC 9(10).99.
           03  CLKMLOG-B035-TRACK-2-DATA-LEN     PIC 9(02).
           03  CLKMLOG-B035-TRACK-2-DATA         PIC X(37).
           03  CLKMLOG-B037-RETRIEVAL-REF-NO     PIC X(12).
           03  CLKMLOG-B038-APPROVAL-CODE        PIC X(06).
           03  CLKMLOG-B039-ACTION-CODE          PIC 9(03).
           03  CLKMLOG-B041-CARD-ACPTOR-TERM     PIC X(08).
           03  CLKMLOG-B042-CARD-ACPTOR-IDEN     PIC X(15).
           03  CLKMLOG-B043-CACPTOR-NLOC-LEN     PIC 9(02).
           03  CLKMLOG-B043-CARD-ACPTOR-NLOC     PIC X(99).
           03  CLKMLOG-B044-ADDITION-RESP-LEN    PIC 9(02).
           03  CLKMLOG-B044-ADDITIONAL-RESP      PIC X(99).
           03  CLKMLOG-B045-TRACK-1-DATA-LEN     PIC 9(02).
           03  CLKMLOG-B045-TRACK-1-DATA         PIC X(76).
           03  CLKMLOG-B048-ADDTL-DATA-LEN       PIC 9(03).
           03  CLKMLOG-B048-ADDTL-DATA           PIC X(999).
      *
      * DE48 REQUEST - CCPS - PREVIOUS STATEMENT ENQUIRY
           03  ML48-CCPS REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CCPS-COMMON-PFX          PIC X(150).
               05  MIC003-B048-CCPS-STMT-CYCLE   PIC X(02).
               05  MIC003-B048-SCLT-REL          PIC X(01).
               05  MIC003-B048-SCLS-STMT-CYCLE-YM  PIC 9(06).
               05  FILLER                        PIC X(840).
      *
      * DE48 REQUEST - CCBP - BONUS-POINT REDEMPTION
           03  ML48-CCBP REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CCBP-COMMON-PFX          PIC X(150).
               05  MIC003-B048-CCBP-ACCT-NMBR    PIC 9(16).
               05  FILLER                        PIC X(833).
      *
      * DE48 REQUEST - PYMT - CASH/CHEQUE PAYMENT
           03  ML48-PYMT REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-PYMT-COMMON-PFX          PIC X(150).
               05  MIC003-B048-PYMT-ACCT-NMBR    PIC 9(16).
               05  MIC003-B048-PYMT-MYCLR-TXN-IND  PIC X(01).
               05  MIC003-B048-PYMT-MYCLR-RR     PIC X(20).
               05  MIC003-B048-PYMT-MYCLR-DESC   PIC X(20).
               05  MIC003-B048-PYMT-MYCLR-NAME   PIC X(80).
               05  MIC003-B048-PYMT-FROM-ACCT    PIC X(19).
               05  MIC003-B048-PYMT-TRXN-TYPE    PIC X(03).
               05  MIC003-B048-PYMT-INDICATOR    PIC X(04).
               05  MIC003-B048-PYMT-MTID         PIC X(28).
               05  MIC003-B048-PYMT-DUPL-FLAG    PIC X(01).
               05  MIC003-B048-PYMT-SAF-IND      PIC X(01).
               05  MIC003-B048-PYMT-BIZMSG-IDR   PIC X(30).
               05  MIC003-B048-PYMT-MER-IND      PIC X(01).
               05  FILLER                        PIC X(625).
      *
      * DE48 REQUEST - AUTH - AUTHORIZATION FINANCIAL
           03  ML48-AUTH REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-AUTH-COMMON-PFX          PIC X(150).
               05  MIC003-B048-AUTH-REVERSAL-DATA  PIC X(42).
               05  MIC003-B048-AUTH-FILLER       PIC X(712).
               05  MIC003-B048-PARTIAL-APPR-IND  PIC X(01).
               05  FILLER                        PIC X(94).
      *
      * DE48 REQUEST - CASH - CASH ADVANCE
           03  ML48-CASH REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CASH-COMMON-PFX          PIC X(150).
               05  MIC003-B048-CASH-GL-REFERENCE  PIC X(30).
               05  MIC003-B048-CASH-TC-CODE      PIC X(04).
               05  MIC003-B048-CASH-DESCRIPTION  PIC X(35).
               05  MIC003-B048-CASH-MYCLR-TXN-IND  PIC X(01).
               05  MIC003-B048-CASH-MYCLR-RR     PIC X(20).
               05  MIC003-B048-CASH-MYCLR-DESC   PIC X(20).
               05  MIC003-B048-CASH-TO-ACCT      PIC X(19).
               05  MIC003-B048-CASH-DOC-NO       PIC X(20).
               05  MIC003-B048-CASH-TRXN-TYPE    PIC X(03).
               05  FILLER                        PIC X(697).
      *
      * DE48 REQUEST - RTL - RETAIL DEBIT
           03  ML48-RTL REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-RTL-COMMON-PFX           PIC X(150).
               05  MIC003-B048-RTL-GL-REFERENCE  PIC X(30).
               05  MIC003-B048-RTL-TC-CODE       PIC X(04).
               05  MIC003-B048-RTL-DESCRIPTION   PIC X(35).
               05  MIC003-B048-RTL-DOC-NO        PIC X(20).
               05  MIC003-B048-RTL-GST-CDE       PIC X(03).
               05  MIC003-B048-RTL-GST-AMT       PIC 9(5)V99.
               05  MIC003-B048-RTL-FROM-ACCT     PIC X(19).
               05  MIC003-B048-RTL-TRXN-TYPE     PIC X(03).
               05  MIC003-B048-RTL-INDICATOR     PIC X(04).
               05  MIC003-B048-RTL-MTID          PIC X(28).
               05  MIC003-B048-RTL-MYCLR-TXN-IND  PIC X(01).
               05  MIC003-B048-RTL-MYCLR-RR      PIC X(20).
               05  MIC003-B048-RTL-MYCLR-DESC    PIC X(20).
               05  MIC003-B048-RTL-MYCLR-NAME    PIC X(80).
               05  FILLER                        PIC X(575).
      *
      * DE48 REQUEST - ECOM - E-COMMERCE REQUEST
           03  ML48-ECOM REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-ECOM-COMMON-PFX          PIC X(150).
               05  MIC003-B048-ECOM-TXN-IND      PIC X(01).
               05  MIC003-B048-ECOM-USERID       PIC X(08).
               05  MIC003-B048-ECOM-CVV2-CVC2    PIC X(03).
               05  MIC003-B048-ECOM-INSTALMENT-PL  PIC 9(03).
               05  MIC003-B048-ECOM-PAYMENT-TERM  PIC 9(02).
               05  MIC003-B048-ECOM-INTEREST-RATE  PIC 9V9(05).
               05  MIC003-B048-ECOM-SEC-DATA     PIC X(90).
               05  MIC003-B048-ECOM-PNBR         PIC X(15).
               05  MIC003-B048-ECOM-ADDTL-DATA   PIC X(150).
               05  FILLER                        PIC X(571).
      *
      * DE48 REQUEST - ECOM-REV - E-COMMERCE REVERSAL
           03  ML48-ECOM-REV REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-ECOM-REV-COMMON-PFX      PIC X(150).
               05  MIC003-B048-ECOM-REV-IND      PIC X(01).
               05  FILLER                        PIC X(848).
      *
      * DE48 REQUEST - CPVU - CONTACTLESS VALUE UPDATE
           03  ML48-CPVU REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CPVU-COMMON-PFX          PIC X(150).
               05  MIC003-B048-CPVU-CNTLES-LMT   PIC 9(11).
               05  FILLER                        PIC X(838).
      *
      * DE48 REQUEST - CCAA - CUSTOMER ADDRESS/CONTACT MAINT
           03  ML48-CCAA REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CCAA-COMMON-PFX          PIC X(150).
               05  MIC003-B048-CCAA-CUST-ORG     PIC 9(03).
               05  MIC003-B048-CCAA-CUST-NMBR    PIC 9(16).
               05  MIC003-B048-CCAA-CARD-TYPE    PIC 9(03).
               05  MIC003-B048-CCAA-ACCOUNT-NMBR  PIC 9(16).
               05  MIC003-B048-CCAA-NAME-LINE-1  PIC X(30).
               05  MIC003-B048-CCAA-NAME-LINE-2  PIC X(30).
               05  MIC003-B048-CCAA-SHORT-NAME   PIC X(15).
               05  MIC003-B048-CCAA-ADD-LINE-1   PIC X(30).
               05  MIC003-B048-CCAA-ADD-LINE-2   PIC X(30).
               05  MIC003-B048-CCAA-CITY         PIC X(28).
               05  MIC003-B048-CCAA-ST-CNTY      PIC X(02).
               05  MIC003-B048-CCAA-ZIP-CD       PIC X(09).
               05  MIC003-B048-CCAA-HOME-PHONE   PIC X(18).
               05  MIC003-B048-CCAA-HANDPHONE    PIC X(18).
               05  MIC003-B048-CCAA-EMAIL        PIC X(30).
               05  MIC003-B048-CCAA-CREDIT-LINE  PIC 9(11).
               05  MIC003-B048-CCAA-EMPLOYER     PIC X(30).
               05  MIC003-B048-CCAA-WORK-PHONE   PIC X(18).
               05  MIC003-B048-CCAA-BILLING-CYCLE  PIC 9(02).
               05  MIC003-B048-CCAA-SEX          PIC 9(01).
               05  MIC003-B048-CCAA-INCOME       PIC 9(09).
               05  MIC003-B048-CCAA-BEHAV-SCORE  PIC 9(03).
               05  MIC003-B048-CCAA-HOME-OWNER   PIC 9(01).
               05  MIC003-B048-CCAA-TYP-OF-RES   PIC X(02).
               05  MIC003-B048-CCAA-ACORN-CODE   PIC X(04).
               05  MIC003-B048-CCAA-LEZ-CODE     PIC X(04).
               05  MIC003-B048-CCAA-BANK-ACCT-IND  PIC X(02).
               05  MIC003-B048-CCAA-MARITAL-STS  PIC 9(01).
               05  MIC003-B048-CCAA-NBR-OF-DEPS  PIC 9(02).
               05  MIC003-B048-CCAA-OCCPN-CODE   PIC X(04).
               05  MIC003-B048-CCAA-PER-OCCPN    PIC 9(04).
               05  MIC003-B048-CCAA-CUST-CLASS   PIC X(02).
               05  MIC003-B048-CCAA-EMPLOYER-CODE  PIC X(04).
               05  MIC003-B048-CCAA-CRT-LIABLE   PIC X(01).
               05  MIC003-B048-CCAA-SMSA         PIC 9(04).
               05  MIC003-B048-CCAA-CENSUS       PIC 9(07).
               05  MIC003-B048-CCAA-EMPL-TYP     PIC X(03).
               05  MIC003-B048-CCAA-MSIC-2008    PIC X(05).
               05  MIC003-B048-CCAA-OKU-IND      PIC X(01).
               05  MIC003-B048-CCAA-LAST-IC      PIC X(25).
               05  MIC003-B048-CCAA-DUP-STMT-ORG  PIC 9(03).
               05  MIC003-B048-CCAA-DUP-STMT-NBR  PIC 9(16).
               05  MIC003-B048-CCAA-ACC-CYCLE    PIC 9(02).
               05  MIC003-B048-CCAA-AGENT-BANK   PIC 9(05).
               05  MIC003-B048-CCAA-SH-NAME      PIC X(15).
               05  MIC003-B048-CCAA-USER-CODE-1  PIC X(02).
               05  MIC003-B048-CCAA-USER-CODE-2  PIC X(02).
               05  MIC003-B048-CCAA-USER-CODE-3  PIC X(02).
               05  MIC003-B048-CCAA-USER-CODE-6  PIC X(02).
               05  MIC003-B048-CCAA-CRLIMIT      PIC 9(11).
               05  MIC003-B048-CCAA-SRC-INC      PIC X(03).
               05  MIC003-B048-CCAA-SRC-INC-OTH  PIC X(50).
               05  MIC003-B048-CCAA-RELATIONSHIP  PIC X(01).
               05  MIC003-B048-CCAA-EMBOSS-NAME1  PIC X(26).
               05  MIC003-B048-CCAA-EMBOSS-NAME2  PIC X(26).
               05  MIC003-B048-CCAA-ACCT-ORG     PIC 9(03).
               05  MIC003-B048-CCAA-ACCT-TYPE    PIC 9(03).
               05  MIC003-B048-CCAA-ACCT-NMBR    PIC 9(16).
               05  MIC003-B048-CCAA-ACCT-CURR-CD  PIC 9(03).
               05  MIC003-B048-CCAA-PLT-CYCLE    PIC 9(02).
               05  MIC003-B048-CCAA-CUSTOMER-ORG  PIC 9(03).
               05  MIC003-B048-CCAA-CUSTOMER-ID  PIC 9(16).
               05  MIC003-B048-CCAA-SUP-CUST-ORG  PIC 9(03).
               05  MIC003-B048-CCAA-SUP-CUST-ID  PIC 9(16).
               05  MIC003-B048-CCAA-USER-DATA-2  PIC X(20).
               05  MIC003-B048-CCAA-PRD-TYP      PIC X(01).
               05  MIC003-B048-CCAA-CUS-TYP      PIC X(01).
               05  MIC003-B048-CCAA-PRN-DAT-FLD-1  PIC X(20).
               05  MIC003-B048-CCAA-PRN-DAT-FLD-2  PIC X(20).
               05  MIC003-B048-CCAA-PRD-IND-1    PIC X(01).
               05  MIC003-B048-CCAA-PRD-IND-2    PIC X(01).
               05  MIC003-B048-CCAA-PRD-IND-3    PIC X(01).
               05  MIC003-B048-CCAA-OTH-IND      PIC 9(01).
               05  FILLER                        PIC X(124).
      *
      * DE48 REQUEST - CCMC - CUSTOMER ADDRESS/CONTACT MAINT
           03  ML48-CCMC REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CCMC-COMMON-PFX          PIC X(150).
               05  MIC003-B048-CCMC-HOME-PHONE   PIC X(18).
               05  MIC003-B048-CCMC-MOBILE-PHONE  PIC X(18).
               05  MIC003-B048-CCMC-OFFICE-PHONE  PIC X(18).
               05  MIC003-B048-CCMC-EMAIL-ADDRESS  PIC X(50).
               05  MIC003-B048-CCMC-NAME-1       PIC X(30).
               05  MIC003-B048-CCMC-NAME-2       PIC X(30).
               05  MIC003-B048-CCMC-NAME-3       PIC X(30).
               05  MIC003-B048-CCMC-ADDR-1       PIC X(30).
               05  MIC003-B048-CCMC-ADDR-2       PIC X(30).
               05  MIC003-B048-CCMC-CITY         PIC X(28).
               05  MIC003-B048-CCMC-STATE        PIC X(2).
               05  MIC003-B048-CCMC-ZIP-CODE     PIC X(9).
               05  MIC003-B048-CCMC-ADDL-ADDR-1  PIC X(30).
               05  MIC003-B048-CCMC-ADDL-ADDR-2  PIC X(30).
               05  MIC003-B048-CCMC-ADDL-ADDR-3  PIC X(30).
               05  MIC003-B048-CCMC-ADDL-CITY    PIC X(30).
               05  MIC003-B048-CCMC-ADDL-ZIP     PIC X(22).
               05  MIC003-B048-CCMC-ADDL-EXP-DATE  PIC 9(08).
               05  FILLER                        PIC X(406).
      *
      * DE48 REQUEST - CCCP - PERM CREDIT-LIMIT MAINT
           03  ML48-CCCP REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CCCP-COMMON-PFX          PIC X(150).
               05  MIC003-B048-CCCP-CRLIMIT1     PIC 9(09).
               05  MIC003-B048-CCCP-CRLIMIT2     PIC 9(09).
               05  MIC003-B048-CCCP-CRLINE       PIC 9(11).
               05  MIC003-B048-CCCP-RTLLIMIT     PIC 9(10).
               05  MIC003-B048-CCCP-CTD-RTLLIMIT  PIC 9(15).
               05  MIC003-B048-CCCP-CSHLIMIT     PIC 9(10).
               05  MIC003-B048-CCCP-CTD-CSHLIMIT  PIC 9(15).
               05  MIC003-B048-CCCP-BNM-CAT-CDE  PIC 9(02).
               05  MIC003-B048-CCCP-BNM-REASON   PIC X(200).
               05  MIC003-B048-CCCP-BPP          PIC 9(09)V99.
               05  MIC003-B048-CCCP-BSP          PIC 9(09)V99.
               05  MIC003-B048-CCCP-TTL-PROFIT   PIC 9(09)V99.
               05  MIC003-B048-CCCP-UNEARNED-PFT  PIC 9(09)V99.
               05  FILLER                        PIC X(524).
      *
      * DE48 REQUEST - CCCT - TEMP CREDIT-LIMIT MAINT
           03  ML48-CCCT REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CCCT-COMMON-PFX          PIC X(150).
               05  MIC003-B048-CCCT-CRLIMIT1     PIC 9(09).
               05  MIC003-B048-CCCT-CRLIMIT1-EFF  PIC 9(08).
               05  MIC003-B048-CCCT-CRLIMIT1-EXP  PIC 9(08).
               05  MIC003-B048-CCCT-CRLIMIT2     PIC 9(09).
               05  MIC003-B048-CCCT-CRLIMIT2-EFF  PIC 9(08).
               05  MIC003-B048-CCCT-CRLIMIT2-EXP  PIC 9(08).
               05  MIC003-B048-CCCT-CRLINE       PIC 9(11).
               05  MIC003-B048-CCCT-CRLINE-EFF   PIC 9(08).
               05  MIC003-B048-CCCT-CRLINE-EXP   PIC 9(08).
               05  MIC003-B048-CCCT-RTLLIMIT     PIC 9(10).
               05  MIC003-B048-CCCT-CTD-RTLLIMIT  PIC 9(15).
               05  MIC003-B048-CCCT-CSHLIMIT     PIC 9(10).
               05  MIC003-B048-CCCT-CTD-CSHLIMIT  PIC 9(15).
               05  MIC003-B048-CCCT-PLIMIT-EFF   PIC 9(08).
               05  MIC003-B048-CCCT-PLIMIT-EXP   PIC 9(08).
               05  FILLER                        PIC X(706).
      *
      * DE48 REQUEST - CCAV-IVR - CARD ACTIVATION (IVR)
           03  ML48-CCAV-IVR REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CCAV-IVR-COMMON-PFX      PIC X(150).
               05  MIC003-B048-CCAV-IVR-MOBILE   PIC X(18).
               05  FILLER                        PIC X(831).
      *
      * DE48 REQUEST - CCOP - SET PAYMENT METHOD
           03  ML48-CCOP REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CCOP-COMMON-PFX          PIC X(150).
               05  MIC003-B048-CCOP-PYMT-METHOD  PIC 9(01).
               05  MIC003-B048-CCOP-DB-NMBR      PIC 9(16).
               05  MIC003-B048-CCOP-ACCT-NMBR    PIC 9(16).
               05  FILLER                        PIC X(816).
      *
      * DE48 REQUEST - CCFU - CARD-NOT-PRESENT FLAG UPDATE
           03  ML48-CCFU REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CCFU-COMMON-PFX          PIC X(150).
               05  MIC003-B048-CCFU-FLAG         PIC X(01).
               05  FILLER                        PIC X(848).
      *
      * DE48 REQUEST - COFU - OVERSEAS FLAG UPDATE
           03  ML48-COFU REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-COFU-COMMON-PFX          PIC X(150).
               05  MIC003-B048-COFU-FLAG         PIC X(01).
               05  MIC003-B048-COFU-START-DATE   PIC 9(08).
               05  MIC003-B048-COFU-END-DATE     PIC 9(08).
               05  FILLER                        PIC X(832).
      *
      * DE48 REQUEST - CPCG - CHIP&PIN PIN CHANGE
           03  ML48-CPCG REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CPCG-COMMON-PFX          PIC X(150).
               05  MIC003-B048-CPCG-NEW-PIN-BLK  PIC X(16).
               05  FILLER                        PIC X(833).
      *
      * DE48 REQUEST - PINC - PIN CHANGE
           03  ML48-PINC REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-PINC-COMMON-PFX          PIC X(150).
               05  MIC003-B048-PINC-NEW-PIN-BLK  PIC X(16).
               05  FILLER                        PIC X(833).
      *
      * DE48 REQUEST - CPRQ - PIN REQUEST
           03  ML48-CPRQ REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CPRQ-COMMON-PFX          PIC X(150).
               05  MIC003-B048-CPRQ-CARD-ACTION  PIC 9(01).
               05  MIC003-B048-CPRQ-USER-ID      PIC X(08).
               05  FILLER                        PIC X(840).
      *
      * DE48 REQUEST - CCRT - CARD REISSUE
           03  ML48-CCRT REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-CCRT-COMMON-PFX          PIC X(150).
               05  MIC003-B048-CCRT-GL-REF       PIC X(30).
               05  MIC003-B048-CCRT-RA-TC        PIC X(04).
               05  MIC003-B048-CCRT-RA-AMT       PIC 9(10)V99.
               05  MIC003-B048-CCRT-RF-TC        PIC X(04).
               05  MIC003-B048-CCRT-RF-AMT       PIC 9(05)V99.
               05  MIC003-B048-CCRT-SD-TC        PIC X(04).
               05  MIC003-B048-CCRT-SD-AMT       PIC 9(05)V99.
               05  MIC003-B048-CCRT-MC-TC        PIC X(04).
               05  MIC003-B048-CCRT-MC-AMT       PIC 9(05)V99.
               05  MIC003-B048-CCRT-DESCRIPTION  PIC X(35).
               05  MIC003-B048-CCRT-SC-TC        PIC X(04).
               05  MIC003-B048-CCRT-SC-AMT       PIC 9(05)V99.
               05  MIC003-B048-CCRT-CPF-TC       PIC X(04).
               05  MIC003-B048-CCRT-CPF-AMT      PIC 9(05)V99.
               05  MIC003-B048-CCRT-GST-RF-CD    PIC X(03).
               05  MIC003-B048-CCRT-GST-RF-AMT   PIC 9(05)V99.
               05  MIC003-B048-CCRT-GST-SD-CD    PIC X(03).
               05  MIC003-B048-CCRT-GST-SD-AMT   PIC 9(05)V99.
               05  MIC003-B048-CCRT-GST-MC-CD    PIC X(03).
               05  MIC003-B048-CCRT-GST-MC-AMT   PIC 9(05)V99.
               05  MIC003-B048-CCRT-GST-SC-CD    PIC X(03).
               05  MIC003-B048-CCRT-GST-SC-AMT   PIC 9(05)V99.
               05  MIC003-B048-CCRT-GST-CPF-CD   PIC X(03).
               05  MIC003-B048-CCRT-GST-CPF-AMT  PIC 9(05)V99.
               05  MIC003-B048-CCRT-RF-DESC      PIC X(35).
               05  MIC003-B048-CCRT-SD-DESC      PIC X(35).
               05  MIC003-B048-CCRT-MC-DESC      PIC X(35).
               05  MIC003-B048-CCRT-SC-DESC      PIC X(35).
               05  MIC003-B048-CCRT-CPF-DESC     PIC X(35).
               05  MIC003-B048-CCRT-FROM-ACCT    PIC X(19).
               05  MIC003-B048-CCRT-TRXN-TYPE    PIC X(03).
               05  MIC003-B048-CCRT-DOC-NO       PIC X(09).
               05  FILLER                        PIC X(457).
      *
      * DE48 REQUEST - SCAP - SPECIAL CARD-ACCT PROC
           03  ML48-SCAP REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-SCAP-COMMON-PFX          PIC X(150).
               05  MIC003-B048-SCAP-FUNCTION-REQ  PIC X(05).
               05  MIC003-B048-SCAP-USERID       PIC X(08).
               05  FILLER                        PIC X(836).
      *
      * DE48 REQUEST - PRPP - DUITNOW REAL-TIME PAYMENT
           03  ML48-PRPP REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-PRPP-COMMON-PFX          PIC X(150).
               05  MIC003-B048-PRPP-ACCT-NMBR    PIC 9(16).
               05  MIC003-B048-PRPP-MYCLR-TXN-IND  PIC X(01).
               05  MIC003-B048-PRPP-MYCLR-RR     PIC X(140).
               05  MIC003-B048-PRPP-MYCLR-DESC   PIC X(140).
               05  MIC003-B048-PRPP-MYCLR-NAME   PIC X(140).
               05  MIC003-B048-PRPP-FROM-ACCT    PIC X(19).
               05  MIC003-B048-PRPP-TRXN-TYPE    PIC X(03).
               05  MIC003-B048-PRPP-INDICATOR    PIC X(04).
               05  MIC003-B048-PRPP-MTID         PIC X(28).
               05  MIC003-B048-PRPP-DUPL-FLAG    PIC X(01).
               05  MIC003-B048-PRPP-SAF-IND      PIC X(01).
               05  MIC003-B048-PRPP-BIZMSG-IDR   PIC X(30).
               05  MIC003-B048-PRPP-RTP-TRANS-IND  PIC X(01).
               05  MIC003-B048-PRPP-EX-PYM-DTL   PIC X(250).
               05  FILLER                        PIC X(75).
      *
      * DE48 REQUEST - SP2P-1100 - P2P TRANSFER
           03  ML48-SP2P-1100 REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-SP2P-1100-COMMON-PFX     PIC X(150).
               05  MIC003-B048-SP2P-IND          PIC X(03).
               05  MIC003-B048-SP2P-STATUS       PIC X(01).
               05  MIC003-B048-SP2P-GL-REFERENCE  PIC X(30).
               05  MIC003-B048-SP2P-TC-CODE      PIC X(04).
               05  MIC003-B048-SP2P-DESCRIPTION  PIC X(35).
               05  MIC003-B048-SP2P-MYC-IND      PIC X(1).
               05  MIC003-B048-SP2P-RR           PIC X(20).
               05  MIC003-B048-SP2P-OPD          PIC X(20).
               05  MIC003-B048-SP2P-SNM          PIC X(80).
               05  FILLER                        PIC X(655).
      *
      * DE48 REQUEST - GCVM - GET CVM/LIMIT
           03  ML48-GCVM REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-GCVM-COMMON-PFX          PIC X(150).
               05  MIC003-B048-GCVM-OTP-REASON   PIC X(02).
               05  MIC003-B048-GCVM-TRID         PIC X(11).
               05  MIC003-B048-GCVM-TKN-REF-ID   PIC X(32).
               05  MIC003-B048-GCVM-PAN-REF-ID   PIC X(32).
               05  MIC003-B048-GCVM-LIFE-CYC-ID  PIC X(15).
               05  MIC003-B048-GCVM-PAN-SRC      PIC X(02).
               05  MIC003-B048-GCVM-DVC-NMBR     PIC X(13).
               05  FILLER                        PIC X(742).
      *
      * DE48 REQUEST - MAAQ - OCTO ACCOUNT REQUEST
           03  ML48-MAAQ REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-MAAQ-COMMON-PFX          PIC X(150).
               05  MIC003-B048-AQ-CR-IC          PIC X(25).
               05  MIC003-B048-AQ-CR-IC-TYPE     PIC X(02).
               05  FILLER                        PIC X(822).
      *
      * DE48 REQUEST - MSIC - MERCHANT MSIC
           03  ML48-MSIC REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-MSIC-COMMON-PFX          PIC X(150).
               05  MIC003-B048-MSIC-CODE         PIC X(05).
               05  FILLER                        PIC X(844).
      *
      * DE48 REQUEST - MTAM - OCTO ACCOUNT/CARD REQUEST
           03  ML48-MTAM REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-MTAM-COMMON-PFX          PIC X(150).
               05  MIC003-B048-AM-MC-PAID        PIC X(48).
               05  MIC003-B048-AM-CMNT-TXT       PIC X(50).
               05  MIC003-B048-AM-RSN-CODE       PIC X(01).
               05  MIC003-B048-AM-USR-ID         PIC X(50).
               05  MIC003-B048-AM-CR-NAME        PIC X(60).
               05  MIC003-B048-AM-ORG            PIC X(50).
               05  MIC003-B048-AM-CR-PHONE       PIC X(18).
               05  FILLER                        PIC X(572).
      *
      * DE48 REQUEST - MTIM - OCTO/RBK2 INTERFACE
           03  ML48-MTIM REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-MTIM-COMMON-PFX          PIC X(150).
               05  MIC003-B048-IM-EXCL-DEL-IND   PIC X(01).
               05  MIC003-B048-IM-INCL-DVC-IND   PIC X(01).
               05  MIC003-B048-IM-EXCL-TKN-IND   PIC X(01).
               05  MIC003-B048-IM-TKN-STS-CODE   PIC X(01).
               05  MIC003-B048-IM-USR-ID         PIC X(50).
               05  MIC003-B048-IM-USR-NAME       PIC X(60).
               05  MIC003-B048-IM-ORG            PIC X(50).
               05  MIC003-B048-IM-PHONE          PIC X(18).
               05  FILLER                        PIC X(667).
      *
      * DE48 REQUEST - MTKA - TOKEN ACTIVATE
           03  ML48-MTKA REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-MTKA-COMMON-PFX          PIC X(150).
               05  MIC003-B048-KA-MC-PAID        PIC X(48).
               05  MIC003-B048-KA-USR-ID         PIC X(50).
               05  FILLER                        PIC X(751).
      *
      * DE48 REQUEST - MTKM - TOKEN MAINTENANCE
           03  ML48-MTKM REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-MTKM-COMMON-PFX          PIC X(150).
               05  MIC003-B048-TM-TOKEN          PIC X(19).
               05  MIC003-B048-TM-ACTION         PIC X(01).
               05  MIC003-B048-TM-ACTION-DATE    PIC 9(08).
               05  MIC003-B048-TM-REPL-CARD      PIC X(19).
               05  MIC003-B048-TM-REPL-EXPIRY    PIC 9(04).
               05  MIC003-B048-TM-REPL-CARD-SEQ  PIC 9(03).
               05  MIC003-B048-TM-NOTIFY-SVC     PIC X(01).
               05  MIC003-B048-TM-TKN-REF-ID     PIC X(32).
               05  FILLER                        PIC X(762).
      *
      * DE48 REQUEST - MTKP - TOKEN PROVISION
           03  ML48-MTKP REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-MTKP-COMMON-PFX          PIC X(150).
               05  MIC003-B048-MTKP-VISA-TKN-RID  PIC X(32).
               05  MIC003-B048-MTKP-MC-CORREL-ID  PIC X(14).
               05  FILLER                        PIC X(803).
      *
      * DE48 REQUEST - MTKQ - TOKEN INQUIRY
           03  ML48-MTKQ REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-MTKQ-COMMON-PFX          PIC X(150).
               05  MIC003-B048-MTKQ-INQ-PURPOSE  PIC X(01).
               05  MIC003-B048-MTKQ-USER-ID      PIC X(50).
               05  MIC003-B048-MTKQ-USER-NAME    PIC X(60).
               05  FILLER                        PIC X(738).
      *
      * DE48 REQUEST - NBPS - NBPS / NATIONAL PAYMENT
           03  ML48-NBPS REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-NBPS-COMMON-PFX          PIC X(150).
               05  MIC003-B048-NBPS-TRX-IND      PIC X(04).
               05  MIC003-B048-NBPS-BILLER-CODE  PIC X(10).
               05  MIC003-B048-NBPS-BILLER-NAME  PIC X(40).
               05  MIC003-B048-NBPS-RR-NUMBER1   PIC X(20).
               05  MIC003-B048-NBPS-REF-NUM      PIC X(20).
               05  MIC003-B048-NBPS-GL-REF-NUM   PIC X(30).
               05  MIC003-B048-NBPS-MER-IND      PIC X(01).
               05  MIC003-B048-NBPS-BIZ-MSD-ID   PIC X(35).
               05  MIC003-B048-NBPS-RTP-TRANS-IND  PIC X(01).
               05  FILLER                        PIC X(688).
      *
      * DE48 REQUEST - SAIQ - SPECIAL ACCOUNT INQ
           03  ML48-SAIQ REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-SAIQ-COMMON-PFX          PIC X(150).
               05  MIC003-B048-SAIQ-CUST-ORG     PIC 9(03).
               05  MIC003-B048-SAIQ-CUST-NBR     PIC 9(16).
               05  FILLER                        PIC X(830).
      *
      * DE48 REQUEST - SCIK - SPECIAL CARDHOLDER LIST
           03  ML48-SCIK REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-SCIK-COMMON-PFX          PIC X(150).
               05  MIC003-B048-SCIK-CUSTOMER-ID  PIC 9(16).
               05  FILLER                        PIC X(833).
      *
      * DE48 REQUEST - SCIQ - SPECIAL CUSTOMER INQ
           03  ML48-SCIQ REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-SCIQ-COMMON-PFX          PIC X(150).
               05  MIC003-B048-SCIQ-CUST-ORG     PIC 9(03).
               05  MIC003-B048-SCIQ-CUST-NBR     PIC 9(16).
               05  MIC003-B048-SCIQ-CUST-ID      PIC X(25).
               05  MIC003-B048-SCIQ-CUST-ID-TYP  PIC X(03).
               05  FILLER                        PIC X(802).
      *
      * DE48 REQUEST - SCTF - SPECIAL TRANSFER
           03  ML48-SCTF REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-SCTF-COMMON-PFX          PIC X(150).
               05  MIC003-B048-SCTF-PLASTIC-NBR  PIC X(19).
               05  MIC003-B048-SCTF-EFF-DATE     PIC 9(08).
               05  MIC003-B048-SCTF-EXP-DATE     PIC 9(04).
               05  MIC003-B048-SCTF-USER-ID      PIC X(08).
               05  FILLER                        PIC X(810).
      *
      * DE48 REQUEST - SICR - SPECIAL INQ RESP
           03  ML48-SICR REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-SICR-COMMON-PFX          PIC X(150).
               05  MIC003-B048-SICR-COLL-BRANCH  PIC 9(05).
               05  MIC003-B048-SICR-USER-ID      PIC X(08).
               05  FILLER                        PIC X(836).
      *
      * DE48 REQUEST - SMCS - SPECIAL MC-STMT
           03  ML48-SMCS REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-SMCS-COMMON-PFX          PIC X(150).
               05  MIC003-B048-SMCS-TNG-MFG-NBR  PIC 9(16).
               05  MIC003-B048-SMCS-REQ-TYPE     PIC X(01).
               05  MIC003-B048-SMCS-REQ-INP-DET  PIC X(16).
               05  MIC003-B048-SMCS-USER-ID      PIC X(08).
               05  FILLER                        PIC X(808).
      *
      * DE48 REQUEST - SMIK - SPECIAL MULTI-INQ
           03  ML48-SMIK REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-SMIK-COMMON-PFX          PIC X(150).
               05  MIC003-B048-SMIK-CUST-ORG     PIC 9(03).
               05  MIC003-B048-SMIK-CUST-NBR     PIC 9(16).
               05  FILLER                        PIC X(830).
      *
      * DE48 REQUEST - SPCD - SPECIAL CARD DATA
           03  ML48-SPCD REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-SPCD-COMMON-PFX          PIC X(150).
               05  MIC003-B048-SPCD-IDENTIFIER   PIC X(02).
               05  MIC003-B048-SPCD-OTP-CD       PIC X(08).
               05  MIC003-B048-SPCD-OTP-EXP      PIC X(19).
               05  MIC003-B048-SPCD-OTP-REASON   PIC X(02).
               05  MIC003-B048-SPCD-TRID         PIC X(11).
               05  FILLER                        PIC X(807).
      *
      * DE48 REQUEST - SPPT - SPECIAL PAYMENT
           03  ML48-SPPT REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-SPPT-COMMON-PFX          PIC X(150).
               05  MIC003-B048-SPPT-ACCT-ORG     PIC 9(03).
               05  MIC003-B048-SPPT-ACCT-TYPE    PIC 9(03).
               05  MIC003-B048-SPPT-ACCT-NMBR    PIC 9(16).
               05  MIC003-B048-SPPT-TRAN-DATE    PIC 9(08).
               05  MIC003-B048-SPPT-TRAN-TIME    PIC 9(07).
               05  MIC003-B048-SPPT-USERID       PIC X(08).
               05  MIC003-B048-SPPT-REQUEST-TYPE  PIC X(01).
               05  MIC003-B048-SPPT-REQUEST-DTLS  PIC X(803).
      *
      * DE48 REQUEST - SPTD - SPECIAL PAYMENT DETAIL
           03  ML48-SPTD REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-SPTD-COMMON-PFX          PIC X(150).
               05  MIC003-B048-SPTD-STATUS-IND   PIC X(01).
               05  FILLER                        PIC X(848).
      *
      * DE48 REQUEST - SPTE - SPECIAL PAYMENT ENTRY
           03  ML48-SPTE REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-SPTE-COMMON-PFX          PIC X(150).
               05  MIC003-B048-SPTE-TXN-IND      PIC X(01).
               05  MIC003-B048-SPTE-USERID       PIC X(08).
               05  MIC003-B048-SPTE-CVV-CVC      PIC 9(03).
               05  MIC003-B048-SPTE-INSTALMENT-PL  PIC 9(03).
               05  MIC003-B048-SPTE-PAYMENT-TERM  PIC 9(02).
               05  MIC003-B048-SPTE-INTEREST-RATE  PIC 9V9(05).
               05  MIC003-B048-SPTE-APPLID       PIC X(20).
               05  MIC003-B048-SPTE-BUN-CL-IND   PIC X(01).
               05  FILLER                        PIC X(805).
      *
      * DE48 REQUEST - VCIC - VISA CUSTOMER INQUIRY
           03  ML48-VCIC REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-VCIC-COMMON-PFX          PIC X(150).
               05  MIC003-B048-VCIC-CUS-NBR1     PIC X(19).
               05  MIC003-B048-VCIC-ID-TY1       PIC X(02).
               05  MIC003-B048-VCIC-CUS-NBR2     PIC X(19).
               05  MIC003-B048-VCIC-ID-TY2       PIC X(02).
               05  FILLER                        PIC X(807).
      *
      * DE48 REQUEST - VCIH - VISA STMT INQ
           03  ML48-VCIH REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-VCIH-COMMON-PFX          PIC X(150).
               05  MIC003-B048-VCIH-CCY          PIC 9(03).
               05  MIC003-B048-VCIH-STMT-DTE     PIC 9(08).
               05  FILLER                        PIC X(838).
      *
      * DE48 REQUEST - VLIC - VISA CHARGEBACK INQ
           03  ML48-VLIC REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-VLIC-COMMON-PFX          PIC X(150).
               05  MIC003-B048-VLIC-HIST-KEY     PIC X(16).
               05  MIC003-B048-VLIC-FILE-IDX     PIC 9(02).
               05  FILLER                        PIC X(831).
      *
      * DE48 REQUEST - VLLC - VISA CHARGEBACK LIST
           03  ML48-VLLC REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-VLLC-COMMON-PFX          PIC X(150).
               05  MIC003-B048-VLLC-ORG-NBR      PIC 9(03).
               05  MIC003-B048-VLLC-DTE-FROM     PIC 9(08).
               05  MIC003-B048-VLLC-DTE-TO       PIC 9(08).
               05  FILLER                        PIC X(830).
      *
      * DE48 REQUEST - VMDR - VISA MDR INQUIRY
           03  ML48-VMDR REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-VMDR-COMMON-PFX          PIC X(150).
               05  MIC003-B048-VMDR-CCY          PIC 9(03).
               05  FILLER                        PIC X(846).
      *
      * DE48 REQUEST - VMI1 - VISA MI INQUIRY
           03  ML48-VMI1 REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-VMI1-COMMON-PFX          PIC X(150).
               05  MIC003-B048-VMI1-INSTL-PLAN   PIC 9(03).
               05  FILLER                        PIC X(846).
      *
      * DE48 REQUEST - VMIC - VISA CONTACT INQUIRY
           03  ML48-VMIC REDEFINES
               CLKMLOG-B048-ADDTL-DATA.
               05  ML48-VMIC-COMMON-PFX          PIC X(150).
               05  MIC003-B048-VMIC-CNT-ID       PIC X(06).
               05  FILLER                        PIC X(843).
           03  CLKMLOG-B049-TRXN-CURR-CODE       PIC 9(03).
           03  CLKMLOG-B052-PIN-DATA             PIC X(16).
           03  CLKMLOG-B054-AMOUNT-ADDTL-LEN     PIC 9(03).
           03  CLKMLOG-B054-AMOUNT-ADDTL-DATA    PIC X(120).
           03  CLKMLOG-B056-ORIGINAL-DATA-LEN    PIC 9(02).
           03  CLKMLOG-B056-ORIG-MTI             PIC 9(04).
           03  CLKMLOG-B056-ORIG-STN             PIC 9(06).
           03  CLKMLOG-B056-ORIG-LDT             PIC 9(12).
           03  CLKMLOG-B056-ORIG-AII-LEN         PIC 9(02).
           03  CLKMLOG-B056-ORIG-AII             PIC 9(11).
           03  CLKMLOG-B060-OUTPUT-DATA-1-LEN    PIC 9(03).
           03  CLKMLOG-B060-OUTPUT-DATA-1        PIC X(999).
      *
      * DE60 RESPONSE - CCPS - MIC002-STATEMENT-INQ-REC
           03  ML60-CCPS REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-SECOND-ACCT-IND        PIC X(01).
               05  MIC002-HOST-DATE-TIME         PIC 9(14).
               05  MIC002-CR-LIMIT               PIC 9(09).
               05  MIC002-CUR-BAL                PIC 9(09)V99.
               05  MIC002-CUR-BAL-IND            PIC X(01).
               05  MIC002-PREV-BAL               PIC 9(09)V99.
               05  MIC002-PREV-BAL-IND           PIC X(01).
               05  MIC002-OTHER-HEADER           PIC X(29).
               05  MIC002-NO-OF-TRANS-DTL        PIC 9(02).
               05  MIC002-TX-POST-DATE           PIC X(08).
               05  MIC002-TX-DATE                PIC X(08).
               05  MIC002-TX-DESC                PIC X(40).
               05  MIC002-TX-AMT                 PIC X(12).
               05  MIC002-TX-AMT-IND             PIC X(01).
               05  MIC002-TX-REF-NO              PIC X(23).
               05  MIC002-CARD-NMBR              PIC X(19).
               05  MIC002-TX-CODE                PIC 9(04).
               05  MIC002-MCC                    PIC 9(04).
               05  MIC002-POS-MODE               PIC X(02).
               05  MIC002-XBORDER-AMT            PIC S9(07)V99.
               05  MIC002-MARKUP-AMT             PIC S9(07)V99.
               05  MIC002-CCA-AMT                PIC S9(07)V99.
               05  FILLER                        PIC X(15).
               05  FILLER                        PIC X(757).
      *
      * DE60 RESPONSE - CCBP - MIC002-BONUS-REDEMPTION-REC
           03  ML60-CCBP REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-BP-UPDATED-BALANCE     PIC 9(10).
               05  MIC002-BP-UPDATED-USED-CTD    PIC 9(10).
               05  FILLER                        PIC X(979).
      *
      * DE60 RESPONSE - PYMT - MIC002-PYMT-RESP-INFO-REC
           03  ML60-PYMT REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-PYMT-BANK-CODE         PIC 9(02).
               05  MIC002-PYMT-BRANCH-CODE       PIC 9(05).
               05  MIC002-PYMT-GL-REFERENCE      PIC X(20).
               05  MIC002-PYMT-REASON-CODE       PIC X(02).
               05  MIC002-PYMT-P2P-TRANS-DESC    PIC X(53).
               05  MIC002-PYMT-TC-CODE           PIC X(04).
               05  MIC002-PYMT-CURR-BALANCE      PIC 9(10)V99.
               05  MIC002-PYMT-CURR-BALANCE-IND  PIC X(01).
               05  MIC002-PYMT-CO-AVL-CRE        PIC 9(12)V99.
               05  MIC002-PYMT-CO-AVL-CRE-IND    PIC X(01).
               05  MIC002-PYMT-CR-AVL-CRE        PIC 9(12)V99.
               05  MIC002-PYMT-CR-AVL-CRE-IND    PIC X(01).
               05  MIC002-PYMT-CM-AVL-CRE        PIC 9(12)V99.
               05  MIC002-PYMT-CM-AVL-CRE-IND    PIC X(01).
               05  MIC002-PYMT-PL-AVL-CRE        PIC 9(12)V99.
               05  MIC002-PYMT-PL-AVL-CRE-IND    PIC X(01).
               05  MIC002-PYMT-ACCT-NAME         PIC X(140).
               05  MIC002-PYMT-ACCT-TYP          PIC X(04).
               05  MIC002-PYMT-RSDN-ST           PIC X(01).
               05  MIC002-PYMT-PROD-TYP          PIC X(01).
               05  MIC002-PYMT-SHARIAH-CMPL      PIC X(01).
               05  MIC002-PYMT-DETAILS           PIC X(01).
               05  MIC002-PYMT-CUST-CATEGORY     PIC X(03).
               05  FILLER                        PIC X(689).
      *
      * DE60 RESPONSE - ECOM - MIC002-ECOM-RESP-INFO-REC
           03  ML60-ECOM REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-EI-INSTL-PLAN          PIC 9(03).
               05  MIC002-EI-PAY-TERM            PIC 9(02).
               05  MIC002-EI-COMPUTE-METHOD      PIC 9(01).
               05  MIC002-EI-INTR-RATE           PIC 9V9(5).
               05  MIC002-EI-INTR-FREE-MOS       PIC 9(02).
               05  MIC002-EI-FIRST-PAY-AMT       PIC 9(10)V99.
               05  MIC002-EI-LAST-PAY-AMT        PIC 9(10)V99.
               05  MIC002-EI-MON-INSTL-AMT       PIC 9(10)V99.
               05  MIC002-EI-TOTAL-INSTL-AMT     PIC 9(10)V99.
               05  MIC002-EI-OUTS-PRINCIPAL      PIC 9(10)V99.
               05  MIC002-EI-OUTS-INTEREST       PIC 9(10)V99.
               05  MIC002-EI-HANDLING-FEE        PIC 9(10)V99.
               05  MIC002-EI-PLAN-TYPE           PIC X(01).
               05  MIC002-EI-PROMOTION-FLAG      PIC X(01).
               05  MIC002-EI-WAIVE-FR-MOS        PIC 9(02).
               05  MIC002-EI-WAIVE-TO-MOS        PIC 9(02).
               05  MIC002-EI-PLAN-ORG            PIC 9(03).
               05  MIC002-EI-DBA-NAME            PIC X(25).
               05  MIC002-ECOM-TRXN-CURR-EXPN    PIC 9(01).
               05  MIC002-ECOM-IPM-DATA-CODE     PIC X(12).
               05  FILLER                        PIC X(854).
      *
      * DE60 RESPONSE - MTIM - MIC002-MTIM-INQ-REC
           03  ML60-MTIM REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-IM-PYMT-APP-INST-ID    PIC X(48).
               05  MIC002-IM-DEVICE-NAME         PIC X(64).
               05  MIC002-IM-CURR-STS-CDE        PIC X(01).
               05  MIC002-IM-CURR-STS-DTE        PIC X(25).
               05  MIC002-IM-PROV-STS-CDE        PIC X(01).
               05  MIC002-IM-PROV-STS-DTE        PIC X(25).
               05  MIC002-IM-TKN-REQ-NAME        PIC X(100).
               05  MIC002-IM-PAN-SRC             PIC X(64).
               05  FILLER                        PIC X(372).
               05  FILLER                        PIC X(299).
      *
      * DE60 RESPONSE - MTKP - MIC002-MTKP-INQ-REC
           03  ML60-MTKP REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-MTKP-DATA              PIC X(700).
               05  FILLER                        PIC X(299).
      *
      * DE60 RESPONSE - MTKQ - MIC002-MTKQ-INQ-REC
           03  ML60-MTKQ REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-TQ-SCHME               PIC X(01).
               05  MIC002-TQ-TOKEN               PIC X(19).
               05  MIC002-TQ-DEVICE-IDX          PIC X(02).
               05  MIC002-TQ-DATE-CHANGE         PIC 9(08).
               05  MIC002-TQ-TIME-CHANGE         PIC 9(06).
               05  MIC002-TQ-ASSURANCE-LEVEL     PIC X(02).
               05  MIC002-TQ-REQUESTOR-ID        PIC X(11).
               05  MIC002-TQ-STATUS              PIC X(01).
               05  MIC002-TQ-ACTION-DATE         PIC 9(08).
               05  MIC002-TQ-EXPIRY-DATE         PIC 9(04).
               05  MIC002-TQ-PYMT-ACCT-REF       PIC X(29).
               05  MIC002-TQ-FILLER              PIC X(109).
               05  MIC002-TQ-NTWK-TOKEN          PIC X(500).
               05  FILLER                        PIC X(299).
      *
      * DE60 RESPONSE - SAIQ - MIC002-SAIQ-LIST-INQ-REC
           03  ML60-SAIQ REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-SAIQ-CR-STATUS         PIC X(01).
               05  MIC002-SAIQ-B-SCORE           PIC 9(05).
               05  MIC002-SAIQ-B-SCORE-IND       PIC X(01).
               05  MIC002-SAIQ-CRLIMIT-PERM      PIC 9(09).
               05  MIC002-SAIQ-CRLIMIT-TEMP      PIC 9(09).
               05  MIC002-SAIQ-CRLM-TEMP-EFF-DTE  PIC 9(08).
               05  MIC002-SAIQ-CRLM-TEMP-EXP-DTE  PIC 9(08).
               05  MIC002-SAIQ-CM-ORG-NMBR       PIC 9(03).
               05  MIC002-SAIQ-CM-TYPE           PIC 9(03).
               05  MIC002-SAIQ-CM-CARD-NMBR      PIC 9(16).
               05  MIC002-SAIQ-CM-DTE-OPENED     PIC 9(08).
               05  MIC002-SAIQ-CM-STATUS         PIC X(01).
               05  MIC002-SAIQ-CM-CYCLE          PIC 9(02).
               05  MIC002-SAIQ-CM-USER-CODE      PIC X(02).
               05  MIC002-SAIQ-CM-USER-CODE-2    PIC X(02).
               05  MIC002-SAIQ-CM-USER-CODE-3    PIC X(02).
               05  MIC002-SAIQ-CM-USER-CODE-4    PIC X(02).
               05  MIC002-SAIQ-CM-USER-CODE-5    PIC X(02).
               05  MIC002-SAIQ-CM-USER-CODE-6    PIC X(02).
               05  MIC002-SAIQ-CM-BLOCK-CODE     PIC X(01).
               05  MIC002-SAIQ-CM-DTE-BLOCK-CODE  PIC 9(08).
               05  MIC002-SAIQ-CM-ALT-BLOCK-CODE  PIC X(01).
               05  MIC002-SAIQ-CM-DTE-ALT-BLK-CD  PIC 9(08).
               05  MIC002-SAIQ-CM-CRLIMIT        PIC 9(09).
               05  MIC002-SAIQ-CM-CRLIMIT-IND    PIC X(01).
               05  MIC002-SAIQ-CURR-BALANCE      PIC 9(09)V99.
               05  MIC002-SAIQ-CURR-BALANCE-IND  PIC X(01).
               05  MIC002-SAIQ-CASH-BALANCE      PIC 9(09)V99.
               05  MIC002-SAIQ-CASH-BALANCE-IND  PIC X(01).
               05  MIC002-SAIQ-RTL-BALANCE       PIC 9(09)V99.
               05  MIC002-SAIQ-RTL-BALANCE-IND   PIC X(01).
               05  MIC002-SAIQ-HI-BALANCE        PIC 9(09).
               05  MIC002-SAIQ-HI-BALANCE-IND    PIC X(01).
               05  MIC002-SAIQ-CM-NPL-IND        PIC X(01).
               05  MIC002-SAIQ-CM-DELQ-HIST      PIC X(01).
               05  MIC002-SAIQ-LAST-1ST-MTH-PYMT  PIC 9(09)V99.
               05  MIC002-SAIQ-LAST-1ST-MTH-IND  PIC X(01).
               05  MIC002-SAIQ-LAST-2ND-MTH-PYMT  PIC 9(09)V99.
               05  MIC002-SAIQ-LAST-2ND-MTH-IND  PIC X(01).
               05  MIC002-SAIQ-LAST-3RD-MTH-PYMT  PIC 9(09)V99.
               05  MIC002-SAIQ-LAST-3RD-MTH-IND  PIC X(01).
               05  MIC002-SAIQ-LAST-4TH-MTH-PYMT  PIC 9(09)V99.
               05  MIC002-SAIQ-LAST-4TH-MTH-IND  PIC X(01).
               05  MIC002-SAIQ-LAST-5TH-MTH-PYMT  PIC 9(09)V99.
               05  MIC002-SAIQ-LAST-5TH-MTH-IND  PIC X(01).
               05  MIC002-SAIQ-LAST-6TH-MTH-PYMT  PIC 9(09)V99.
               05  MIC002-SAIQ-LAST-6TH-MTH-IND  PIC X(01).
               05  MIC002-SAIQ-LAST-1ST-CYC-BAL  PIC 9(09)V99.
               05  MIC002-SAIQ-LAST-1ST-CYC-IND  PIC X(01).
               05  MIC002-SAIQ-LAST-2ND-CYC-BAL  PIC 9(09)V99.
               05  MIC002-SAIQ-LAST-2ND-CYC-IND  PIC X(01).
               05  MIC002-SAIQ-LAST-3RD-CYC-BAL  PIC 9(09)V99.
               05  MIC002-SAIQ-LAST-3RD-CYC-IND  PIC X(01).
               05  MIC002-SAIQ-LAST-4TH-CYC-BAL  PIC 9(09)V99.
               05  MIC002-SAIQ-LAST-4TH-CYC-IND  PIC X(01).
               05  MIC002-SAIQ-LAST-5TH-CYC-BAL  PIC 9(09)V99.
               05  MIC002-SAIQ-LAST-5TH-CYC-IND  PIC X(01).
               05  MIC002-SAIQ-LAST-6TH-CYC-BAL  PIC 9(09)V99.
               05  MIC002-SAIQ-LAST-6TH-CYC-IND  PIC X(01).
               05  MIC002-SAIQ-PLT-ORG-NMBR      PIC 9(03).
               05  MIC002-SAIQ-PLT-TYPE-NMBR     PIC 9(03).
               05  MIC002-SAIQ-PLT-CARD-NMBR     PIC X(19).
               05  MIC002-SAIQ-PLT-EMBOSSER-NAME1  PIC X(26).
               05  MIC002-SAIQ-PLT-RELATIONSHIP  PIC X(01).
               05  MIC002-SAIQ-PLT-STATUS        PIC X(01).
               05  MIC002-SAIQ-PLT-BLOCK-CODE    PIC X(01).
               05  MIC002-SAIQ-PLT-EXP-DTE       PIC 9(04).
               05  MIC002-SAIQ-PLT-TFT-DTE       PIC 9(08).
               05  MIC002-SAIQ-PLT-ACT-CODE      PIC X(01).
               05  MIC002-SAIQ-PLT-NEW-PLT-NBR   PIC X(19).
               05  MIC002-SAIQ-PLT-NEW-PLT-EXP   PIC 9(04).
               05  MIC002-SAIQ-PLT-PA            PIC 9(01).
               05  MIC002-SAIQ-PLT-ISS-DTE       PIC 9(08).
               05  MIC002-SAIQ-PLT-LAST-EXP-DTE  PIC 9(04).
               05  MIC002-SAIQ-CR-CLT-CRLIMIT    PIC 9(11).
               05  MIC002-SAIQ-CR-CLT-CRAVL      PIC 9(09)V99.
               05  MIC002-SAIQ-CR-AVAIL-CREDIT   PIC 9(09)V99.
               05  MIC002-SAIQ-CR-TEMP-LIMIT     PIC 9(11).
               05  MIC002-SAIQ-CR-OVERPAY        PIC 9(09)V99.
               05  MIC002-SAIQ-CM-CLT-CRLIMIT    PIC 9(11).
               05  MIC002-SAIQ-CM-CLT-CRAVL      PIC 9(09)V99.
               05  MIC002-SAIQ-CM-AVAIL-CREDIT   PIC 9(09)V99.
               05  MIC002-SAIQ-CM-TEMP-LIMIT     PIC 9(11).
               05  MIC002-SAIQ-CM-OVERPAY        PIC 9(09)V99.
               05  MIC002-SAIQ-CM-CPP-IND        PIC X(01).
               05  MIC002-SAIQ-CM-CPP-EFF-DTE    PIC 9(08).
               05  MIC002-SAIQ-TC-USER-LIMIT-6   PIC 9(09)V99.
               05  MIC002-SAIQ-RTL1-BALANCE      PIC 9(09)V99.
               05  FILLER                        PIC X(449).
      *
      * DE60 RESPONSE - SCIQ - MIC002-SCIQ-LIST-INQ-REC
           03  ML60-SCIQ REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-SCIQ-SHORT-NAME        PIC X(15).
               05  MIC002-SCIQ-NAME-1            PIC X(30).
               05  MIC002-SCIQ-NAME-2            PIC X(30).
               05  MIC002-SCIQ-ADDR-1            PIC X(30).
               05  MIC002-SCIQ-ADDR-2            PIC X(30).
               05  MIC002-SCIQ-CITY              PIC X(28).
               05  MIC002-SCIQ-ZIP-CODE          PIC X(09).
               05  MIC002-SCIQ-HOME-PHONE        PIC X(18).
               05  MIC002-SCIQ-HANDPHONE         PIC X(18).
               05  MIC002-SCIQ-EMAIL-ADDR        PIC X(50).
               05  MIC002-SCIQ-EU-MARITAL-STATUS  PIC 9(01).
               05  MIC002-SCIQ-EU-SEX            PIC 9(01).
               05  MIC002-SCIQ-EU-TYPE-OF-RES    PIC X(02).
               05  MIC002-SCIQ-STATE             PIC X(02).
               05  MIC002-SCIQ-SECURITY-QN       PIC X(30).
               05  MIC002-SCIQ-EU-LEZ-CODE       PIC X(04).
               05  MIC002-SCIQ-SMSA              PIC 9(04).
               05  MIC002-SCIQ-CENSUS-TRACT      PIC 9(07).
               05  MIC002-SCIQ-DTE-BIRTH         PIC 9(08).
               05  MIC002-SCIQ-INCOME            PIC 9(09).
               05  MIC002-SCIQ-OFF-PHONE-FLAG    PIC X(01).
               05  MIC002-SCIQ-CO-TAX-ID-TYPE    PIC X(01).
               05  MIC002-SCIQ-FOREIGN-CNTY-IND  PIC X(01).
               05  MIC002-SCIQ-VVIP-FLAG         PIC X(01).
               05  MIC002-SCIQ-CR-STATUS         PIC X(01).
               05  MIC002-SCIQ-ADDNAME-FLAG      PIC X(01).
               05  MIC002-SCIQ-ADDR-3            PIC X(30).
               05  MIC002-SCIQ-PLT-ORG-NMBR      PIC 9(03).
               05  MIC002-SCIQ-PLT-TYPE-NMBR     PIC 9(03).
               05  MIC002-SCIQ-PLT-CARD-NMBR     PIC X(19).
               05  MIC002-SCIQ-PLT-EMBOSSER-NAME1  PIC X(26).
               05  MIC002-SCIQ-PLT-RELATIONSHIP  PIC X(01).
               05  MIC002-SCIQ-PLT-STATUS        PIC X(01).
               05  MIC002-SCIQ-PLT-BLOCK-CODE    PIC X(01).
               05  MIC002-SCIQ-PLT-DETAILS-1V    PIC X(54).
               05  MIC002-SCIQ-PLT-OPT-IND-1V    PIC X(01).
               05  MIC002-SCIQ-PLT-ABC-IND-1V    PIC X(01).
               05  FILLER                        PIC X(527).
      *
      * DE60 RESPONSE - SICR - MIC002-SICR-RESP-INFO-REC
           03  ML60-SICR REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-SICR-CR-NAME-1         PIC X(30).
               05  MIC002-SICR-CR-ADDR-1         PIC X(30).
               05  MIC002-SICR-CR-ADDR-2         PIC X(30).
               05  MIC002-SICR-CR-ZIP-CODE       PIC X(09).
               05  FILLER                        PIC X(900).
      *
      * DE60 RESPONSE - SMIK - MIC002-SMIK-LIST-INQ-REC
           03  ML60-SMIK REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-SMIK-TNG-CARD-NMBR     PIC 9(16).
               05  MIC002-SMIK-TNG-ZNG-IND       PIC X(01).
               05  MIC002-SMIK-TNG-RELOAD-OPT    PIC X(01).
               05  MIC002-SMIK-TNG-MFG-NMBR      PIC 9(16).
               05  MIC002-SMIK-TNG-MFG-RCV-DATE  PIC 9(06).
               05  MIC002-SMIK-TNG-CARD-STATUS   PIC X(01).
               05  MIC002-SMIK-TNG-REN-MFG-NMBR  PIC 9(16).
               05  MIC002-SMIK-TNG-REN-MFG-RCV-DT  PIC 9(06).
               05  MIC002-SMIK-TNG-REN-MFG-EXP-DT  PIC 9(06).
               05  MIC002-SMIK-TNG-REN-MFG-STATUS  PIC X(01).
               05  MIC002-SMIK-TNG-OLD-MFG-NMBR  PIC 9(16).
               05  MIC002-SMIK-TNG-OLD-MFG-RCV-DT  PIC 9(06).
               05  MIC002-SMIK-TNG-OLD-MFG-EXP-DT  PIC 9(06).
               05  FILLER                        PIC X(901).
      *
      * DE60 RESPONSE - SPTE - MIC002-SPTE-RESP-INFO-REC
           03  ML60-SPTE REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-TE-FIRST-INSTL-AMT     PIC 9(10)V99.
               05  MIC002-TE-FIRST-PYMT-DATE     PIC 9(08).
               05  MIC002-TE-MONTHLY-INSTL-AMT   PIC 9(10)V99.
               05  MIC002-TE-LAST-INSTL-AMT      PIC 9(10)V99.
               05  MIC002-TE-LAST-PYMT-DATE      PIC 9(08).
               05  MIC002-TE-OUTSTD-PRINCIPAL    PIC 9(10)V99.
               05  MIC002-TE-OUTSTD-UNEARN-INT   PIC 9(10)V99.
               05  MIC002-TE-IPP-DATE            PIC 9(08).
               05  MIC002-TE-IPP-TIME            PIC 9(07).
               05  FILLER                        PIC X(908).
      *
      * DE60 RESPONSE - VCIH - MIC002-VCIH-STATEMENT-INQ-REC
           03  ML60-VCIH REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-VCIH-DATA-LEN060       PIC 9(03).
               05  MIC002-VCIH-CR-EXT-ACT-NBR    PIC X(30).
               05  MIC002-VCIH-FEE-BASED-SALES   PIC S9(09)V99.
               05  MIC002-VCIH-AVG-TICKET        PIC S9(07)V99.
               05  MIC002-VCIH-TTL-FEES          PIC S9(07)V99.
               05  MIC002-VCIH-TTL-DISC          PIC S9(07)V99.
               05  MIC002-VCIH-EFF-RATE          PIC 9V9(05).
               05  MIC002-VCIH-DBA-NME           PIC X(25).
               05  MIC002-VCIH-DISC-FREQ         PIC 9(02).
               05  MIC002-VCIH-AMT-DISC-GST      PIC S9(7)V99.
               05  MIC002-VCIH-AMT-FEES-GST      PIC S9(7)V99.
               05  FILLER                        PIC X(877).
      *
      * DE60 RESPONSE - VLIC - MIC002-VLIC-CHBK-TXN-INQ
           03  ML60-VLIC REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-VLIC-DATA-LEN060       PIC 9(03).
               05  MIC002-VLIC-TXN-ARN           PIC X(23).
               05  MIC002-VLIC-TXN-CDE           PIC 9(04).
               05  MIC002-VLIC-APPR-CDE          PIC X(06).
               05  MIC002-VLIC-TXN-AMT           PIC 9(10)V99.
               05  MIC002-VLIC-TXN-CCY           PIC 9(03).
               05  MIC002-VLIC-BIL-AMT           PIC 9(10)V99.
               05  MIC002-VLIC-BIL-CCY           PIC 9(03).
               05  MIC002-VLIC-STTL-AMT          PIC 9(10)V99.
               05  MIC002-VLIC-STTL-CCY          PIC X(03).
               05  MIC002-VLIC-POS-MODE          PIC X(02).
               05  MIC002-VLIC-MCC               PIC X(04).
               05  MIC002-VLIC-MERCH-NME         PIC X(30).
               05  MIC002-VLIC-MERCH-ID          PIC X(15).
               05  MIC002-VLIC-EC-SEC-LEVEL      PIC X(03).
               05  MIC002-VLIC-EC-IND            PIC X(01).
               05  MIC002-VLIC-VROL-FIN-ID       PIC X(11).
               05  MIC002-VLIC-VROL-CASE-NO      PIC X(10).
               05  MIC002-VLIC-TERM-ID           PIC X(15).
               05  MIC002-VLIC-TXN-DATE          PIC X(08).
               05  MIC002-VLIC-TXN-TYPE          PIC X(02).
               05  MIC002-VLIC-CHBK-RSN-CDE      PIC X(04).
               05  MIC002-VLIC-ISS-REF-ID        PIC X(10).
               05  MIC002-VLIC-POS-DATA-CDE      PIC X(12).
               05  FILLER                        PIC X(791).
      *
      * DE60 RESPONSE - VLLC - MIC002-VLLC-CHBK-TXN-LIST
           03  ML60-VLLC REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-VLLC-RESP-LEN060       PIC 9(03).
               05  MIC002-VLLC-TXN-ORG           PIC 9(03).
               05  MIC002-VLLC-ARN               PIC X(23).
               05  MIC002-VLLC-ISS-INST-ID       PIC X(11).
               05  MIC002-VLLC-ACQ-INST-ID       PIC X(11).
               05  MIC002-VLLC-TXN-CDE           PIC X(04).
               05  MIC002-VLLC-REV-IND           PIC X(01).
               05  MIC002-VLLC-PROC-DTE          PIC 9(08).
               05  MIC002-VLLC-TXN-AMT           PIC 9(10)V99.
               05  MIC002-VLLC-TXN-CCY           PIC X(03).
               05  MIC002-VLLC-NETW-IND          PIC X(01).
               05  MIC002-VLLC-TXN-DIR           PIC X(01).
               05  MIC002-VLLC-STATUS            PIC X(01).
               05  MIC002-VLLC-UPD-OPER-ID       PIC X(20).
               05  MIC002-VLLC-HIST-KEY          PIC X(16).
               05  MIC002-VLLC-FIL-IDX           PIC 9(02).
               05  FILLER                        PIC X(879).
      *
      * DE60 RESPONSE - VMDR - MIC002-VMDR-MDR-INQ-REC
           03  ML60-VMDR REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-VMDR-RESP-LEN060       PIC 9(03).
               05  MIC002-VMDR-PROG-OFFER-ID     PIC X(06).
               05  MIC002-VMDR-ID                PIC X(06).
               05  MIC002-VMDR-SCHEME            PIC X(01).
               05  MIC002-VMDR-DISC              PIC X(20).
               05  MIC002-VMDR-RESP-LEN061       PIC 9(03).
               05  MIC002-VMDR-DISC-PLAN         PIC X(06).
               05  MIC002-VMDR-DISC-PLAN-DESC    PIC X(30).
               05  MIC002-VMDR-T1-LOWER-LMT      PIC 9(10)V99.
               05  MIC002-VMDR-T1-ITL-RTE        PIC 9(2)V9(05).
               05  MIC002-VMDR-T1-ITL-FLT        PIC 9(10)V99.
               05  MIC002-VMDR-T1-DOM-RTE        PIC 9(2)V9(05).
               05  MIC002-VMDR-T1-DOM-FLT        PIC 9(10)V99.
               05  MIC002-VMDR-T1-OUS-RTE        PIC 9(2)V9(05).
               05  MIC002-VMDR-T1-OUS-FLT        PIC 9(10)V99.
               05  FILLER                        PIC X(855).
      *
      * DE60 RESPONSE - VMI1 - MIC002-VMI1-RESP-INFO-REC
           03  ML60-VMI1 REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-VMI1-RESP-LEN060       PIC 9(03).
               05  MIC002-VMI1-AMT060            PIC 9(13)V99.
               05  MIC002-VMI1-AMT060-IND        PIC X(01).
               05  MIC002-VMI1-INTR-RATE060      PIC 9(03)V99.
               05  MIC002-VMI1-INT060            PIC 9(13)V99.
               05  MIC002-VMI1-INT060-IND        PIC X(01).
               05  MIC002-VMI1-TENURE-060        PIC 9(03)V99.
               05  MIC002-VMI1-PRIN-INT060       PIC 9(13)V99.
               05  MIC002-VMI1-PRIN-INT060-IND   PIC X(01).
               05  MIC002-VMI1-FIRST-INS060      PIC 9(13)V99.
               05  MIC002-VMI1-FIRST-INS060-IND  PIC X(01).
               05  MIC002-VMI1-MONTH-INS060      PIC 9(13)V99.
               05  MIC002-VMI1-MONTH-INS060-IND  PIC X(01).
               05  MIC002-VMI1-LAST-INS060       PIC 9(13)V99.
               05  MIC002-VMI1-LAST-INS060-IND   PIC X(01).
               05  MIC002-VMI1-EFF-INTR-RATE060  PIC 9(03)V99.
               05  MIC002-VMI1-RESP-LEN061       PIC 9(03).
               05  MIC002-VMI1-TENURE-061        PIC 9(03).
               05  MIC002-VMI1-CYCLE-DATE061     PIC 9(08).
               05  MIC002-VMI1-AMT061            PIC 9(13)V99.
               05  MIC002-VMI1-AMT061-IND        PIC X(01).
               05  MIC002-VMI1-INTR-EARN061      PIC 9(13)V99.
               05  MIC002-VMI1-INTR-EARN061-IND  PIC X(01).
               05  MIC002-VMI1-INTR-UNBIL061     PIC 9(13)V99.
               05  MIC002-VMI1-INTR-UNBIL061-IND  PIC X(01).
               05  MIC002-VMI1-PRIN-AMT061       PIC 9(13)V99.
               05  MIC002-VMI1-PRIN-AMT061-IND   PIC X(01).
               05  MIC002-VMI1-RESP-LEN062       PIC 9(03).
               05  MIC002-VMI1-TENURE-062        PIC 9(03).
               05  MIC002-VMI1-CYCLE-DATE062     PIC 9(08).
               05  MIC002-VMI1-AMT062            PIC 9(13)V99.
               05  MIC002-VMI1-AMT062-IND        PIC X(01).
               05  MIC002-VMI1-INTR-EARN062      PIC 9(13)V99.
               05  MIC002-VMI1-INTR-EARN062-IND  PIC X(01).
               05  MIC002-VMI1-INTR-UNBIL062     PIC 9(13)V99.
               05  MIC002-VMI1-INTR-UNBIL062-IND  PIC X(01).
               05  MIC002-VMI1-PRIN-AMT062       PIC 9(13)V99.
               05  MIC002-VMI1-PRIN-AMT062-IND   PIC X(01).
               05  MIC002-VMI1-RESP-LEN063       PIC 9(03).
               05  MIC002-VMI1-TENURE-063        PIC 9(03).
               05  MIC002-VMI1-CYCLE-DATE063     PIC 9(08).
               05  MIC002-VMI1-AMT063            PIC 9(13)V99.
               05  MIC002-VMI1-AMT063-IND        PIC X(01).
               05  MIC002-VMI1-INTR-EARN063      PIC 9(13)V99.
               05  MIC002-VMI1-INTR-EARN063-IND  PIC X(01).
               05  MIC002-VMI1-INTR-UNBIL063     PIC 9(13)V99.
               05  MIC002-VMI1-INTR-UNBIL063-IND  PIC X(01).
               05  MIC002-VMI1-PRIN-AMT063       PIC 9(13)V99.
               05  MIC002-VMI1-PRIN-AMT063-IND   PIC X(01).
               05  MIC002-VMI1-RESP-LEN116       PIC 9(03).
               05  MIC002-VMI1-TENURE-116        PIC 9(03).
               05  MIC002-VMI1-CYCLE-DATE116     PIC 9(08).
               05  MIC002-VMI1-AMT116            PIC 9(13)V99.
               05  MIC002-VMI1-AMT116-IND        PIC X(01).
               05  MIC002-VMI1-INTR-EARN116      PIC 9(13)V99.
               05  MIC002-VMI1-INTR-EARN116-IND  PIC X(01).
               05  MIC002-VMI1-INTR-UNBIL116     PIC 9(13)V99.
               05  MIC002-VMI1-INTR-UNBIL116-IND  PIC X(01).
               05  MIC002-VMI1-PRIN-AMT116       PIC 9(13)V99.
               05  MIC002-VMI1-PRIN-AMT116-IND   PIC X(01).
               05  MIC002-VMI1-RESP-LEN117       PIC 9(03).
               05  MIC002-VMI1-TENURE-117        PIC 9(03).
               05  MIC002-VMI1-CYCLE-DATE117     PIC 9(08).
               05  MIC002-VMI1-AMT117            PIC 9(13)V99.
               05  MIC002-VMI1-AMT117-IND        PIC X(01).
               05  MIC002-VMI1-INTR-EARN117      PIC 9(13)V99.
               05  MIC002-VMI1-INTR-EARN117-IND  PIC X(01).
               05  MIC002-VMI1-INTR-UNBIL117     PIC 9(13)V99.
               05  MIC002-VMI1-INTR-UNBIL117-IND  PIC X(01).
               05  MIC002-VMI1-PRIN-AMT117       PIC 9(13)V99.
               05  MIC002-VMI1-PRIN-AMT117-IND   PIC X(01).
               05  FILLER                        PIC X(495).
      *
      * DE60 RESPONSE - VMIC - MIC002-VMIC-CONTACT-INQ-REC
           03  ML60-VMIC REDEFINES
               CLKMLOG-B060-OUTPUT-DATA-1.
               05  MIC002-VMIC-DATA-LEN060       PIC 9(03).
               05  MIC002-VMIC-STATUS            PIC X(01).
               05  MIC002-VMIC-OWN-ID            PIC X(01).
               05  MIC002-VMIC-PSL-IDN           PIC X(30).
               05  MIC002-VMIC-PSL-NME-1         PIC X(30).
               05  MIC002-VMIC-PSL-NME-2         PIC X(30).
               05  MIC002-VMIC-ADR-1             PIC X(30).
               05  MIC002-VMIC-ADR-2             PIC X(30).
               05  MIC002-VMIC-ADR-3             PIC X(30).
               05  MIC002-VMIC-ADR-4             PIC X(30).
               05  MIC002-VMIC-STE               PIC X(02).
               05  MIC002-VMIC-CTY               PIC X(13).
               05  MIC002-VMIC-CRY               PIC X(03).
               05  MIC002-VMIC-HOME-CRY          PIC X(03).
               05  MIC002-VMIC-PST-CDE           PIC X(10).
               05  MIC002-VMIC-TEL-1             PIC X(30).
               05  MIC002-VMIC-TEL-2             PIC X(30).
               05  MIC002-VMIC-TEL-3             PIC X(30).
               05  MIC002-VMIC-FAX               PIC X(30).
               05  MIC002-VMIC-EML               PIC X(66).
               05  MIC002-VMIC-MMO               PIC X(66).
               05  MIC002-VMIC-MER-REG-NME       PIC X(30).
               05  FILLER                        PIC X(471).
           03  CLKMLOG-B061-OUTPUT-DATA-2-LEN    PIC 9(03).
           03  CLKMLOG-B061-OUTPUT-DATA-2        PIC X(999).
           03  CLKMLOG-B062-OUTPUT-DATA-3-LEN    PIC 9(03).
           03  CLKMLOG-B062-OUTPUT-DATA-3        PIC X(999).
           03  CLKMLOG-B063-OUTPUT-DATA-4-LEN    PIC 9(03).
           03  CLKMLOG-B063-OUTPUT-DATA-4        PIC X(999).
           03  CLKMLOG-B116-OUTPUT-DATA-5-LEN    PIC 9(03).
           03  CLKMLOG-B116-OUTPUT-DATA-5        PIC X(999).
           03  CLKMLOG-B117-OUTPUT-DATA-6-LEN    PIC 9(03).
           03  CLKMLOG-B117-OUTPUT-DATA-6        PIC X(999).

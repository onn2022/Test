      *---------------------------------------------------------------*
      * MILOGONL - ONLINE MILOG1/2/3 VSAM (IAM) LOG RECORD LAYOUT     *
      * FOR FILE MANAGER / PROGRAM MAPPING OF THE ONLINE LOG FILES    *
      *   MY: xxxMBI.ONLVSM.MYnnnn.MILOGn  KEYS(42,0) REC(252,8047)   *
      *   SG: xxxMBI.ONLVSM.SGnnnn.MILOGn  KEYS(42,0) REC(252,8349)   *
      *---------------------------------------------------------------*
      * SOURCE: MIC004 (ACTIVITY LOG FILE RECORD) + MIC003 (QUEUE     *
      * FILE ISO/8583 RECORD) + IDCAMS DEFINE MIDFLOG2, MISBIZ FD.    *
      *                                                               *
      * DO NOT USE MILOGDAT / MILOGMAP ON THESE FILES - THOSE MAP THE *
      * FIXED-8000 DAILY BATCH EXTRACT (CLKMLOG.DAT) WHERE THE KEY IS *
      * UNPACKED (50 BYTES DISPLAY).  THE ONLINE RECORD PACKS DATE/   *
      * TIME/TRACE/SEQ AS COMP-3, KEY IS 42 BYTES, AND THE RECORD IS  *
      * VARIABLE LENGTH - MAPPING IT WITH MILOGDAT GIVES =LGTH ON     *
      * EVERY RECORD AND UNREADABLE DATE/TIME COLUMNS.                *
      *                                                               *
      * RECORD TYPES (MIC004-REC-TYPE):                               *
      *   A/B ACTIVITY LOG (MESSAGE)   - DATA AREA = MIC003 RECORD    *
      *   M   SYSTEM CONTROL MAINT LOG - DATA AREA = MAINT IMAGE      *
      *   N/O CIA NON-MONETARY MAINT   - DATA AREA = 84-BYTE DATA     *
      *   X   SYSTEM MESSAGES LOG      - DATA AREA = MESSAGE TEXT     *
      *   S   SMS LOG VIA CMBI (MY)                                   *
      * REC-STATUS: ' ' NORMAL, R REVERSED, D DECLINED, U UNMATCHED   *
      * REVERSAL, M MATCHED REVERSAL, P PRPP DUPLICATE (MY).          *
      *                                                               *
      * BYTE MAP (1-BASED):                                           *
      *   KEY 1-42, MTI 43-45(P), REC-TYPE 46, DATE-STAMP 47-51(P),   *
      *   TIME-STAMP 52-55(P), REC-STATUS 56, POS-DATA-CODE 57-68,    *
      *   CARD-TYPE 69, TXN-IC 70-71, FILLER 72-168,                  *
      *   DATA AREA 169-8047 (MY) / 169-8349 (SG).                    *
      *   FOR TYPE A/B THE DATA AREA IS THE MIC003 RECORD:            *
      *   IDENTIFIER 169-267, MSG-TYPE 268-271, BITMAP 272-399,       *
      *   ISO QUEUE-REC (DE FIELDS INCL DE48/DE60) FROM 400.          *
      *---------------------------------------------------------------*
      * LAYOUT 1 - MALAYSIA (MAX LRECL 8047)                          *
      *---------------------------------------------------------------*
       01  MILOG-ONL-RECORD-MY.
           03  MIC004-LOG-FILE-KEY.
               05  MIC004-CARDHOLDER-NMBR        PIC X(19).
               05  MIC004-ALT-KEY.
                   07  MIC004-TRANSACTION-DATE   PIC S9(08) COMP-3.
                   07  MIC004-TRANSACTION-TIME   PIC S9(06) COMP-3.
                   07  MIC004-DELIVERY-CHANNEL   PIC X(08).
                   07  MIC004-TRACE-NUMBER       PIC S9(06) COMP-3.
                   07  MIC004-SEQUENCE-NUMBER    PIC S9(03) COMP-3.
           03  MIC004-MTI                        PIC S9(04) COMP-3.
           03  MIC004-REC-TYPE                   PIC X(01).
           03  MIC004-DATE-STAMP                 PIC S9(08) COMP-3.
           03  MIC004-TIME-STAMP                 PIC S9(06) COMP-3.
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
      *    ---- TYPE A/B: DATA AREA = MIC003 QUEUE RECORD ----
           03  MIC004-MIC003-REC REDEFINES MIC004-DATA-AREA.
               05  MIC003-DATE-RECEIVED          PIC 9(08).
               05  MIC003-TIME-RECEIVED          PIC 9(06).
               05  MIC003-TERMINAL-ID            PIC X(04).
               05  MIC003-TRACE-IND              PIC X(01).
               05  MIC003-SAVE-AREA              PIC X(50).
               05  MIC003-CARD-TYPE              PIC X(01).
               05  MIC003-IPM-DE22-POS-DATA-CODE PIC X(12).
               05  MIC003-TXN-IC                 PIC X(02).
               05  MIC003-ROUTE-DEST-IND         PIC X(01).
               05  MIC003-TCP-QUEUE              PIC X(08).
               05  FILLER                        PIC X(06).
               05  MIC003-MESSAGE-TYPE-ID        PIC 9(04).
               05  MIC003-BYTE-MAP-IND-REC       PIC X(128).
      *        ISO DE FIELDS (B002..B117 INCL DE48 REQUEST AND
      *        B060-B117 OUTPUT SLOTS) - SEE COPYBOOK MIC003 FOR THE
      *        FULL SUB-LAYOUT; PER-TXN DE48/DE60 REDEFINES ARE THE
      *        MIC003-B048-xxxx-DATA / MIC002 GROUPS.
               05  MIC003-QUEUE-REC              PIC X(7648).
      *---------------------------------------------------------------*
      * LAYOUT 2 - SINGAPORE (MAX LRECL 8349)                         *
      * SAME STRUCTURE; IDENTIFIER AREA HAS NO ROUTE-DEST-IND AND     *
      * QUEUE-REC IS X(7950).  FIELD NAMES SUFFIXED -SG.              *
      *---------------------------------------------------------------*
       01  MILOG-ONL-RECORD-SG.
           03  MIC004-LOG-FILE-KEY-SG.
               05  MIC004-CARDHOLDER-NMBR-SG     PIC X(19).
               05  MIC004-ALT-KEY-SG.
                   07  MIC004-TRANS-DATE-SG      PIC S9(08) COMP-3.
                   07  MIC004-TRANS-TIME-SG      PIC S9(06) COMP-3.
                   07  MIC004-DELIVERY-CHNL-SG   PIC X(08).
                   07  MIC004-TRACE-NUMBER-SG    PIC S9(06) COMP-3.
                   07  MIC004-SEQUENCE-NBR-SG    PIC S9(03) COMP-3.
           03  MIC004-MTI-SG                     PIC S9(04) COMP-3.
           03  MIC004-REC-TYPE-SG                PIC X(01).
           03  MIC004-DATE-STAMP-SG              PIC S9(08) COMP-3.
           03  MIC004-TIME-STAMP-SG              PIC S9(06) COMP-3.
           03  MIC004-REC-STATUS-SG              PIC X(01).
           03  MIC004-NETWK-POS-DATA-CD-SG       PIC X(12).
           03  MIC004-CARD-TYPE-SG               PIC X(01).
           03  MIC004-TXN-IC-SG                  PIC X(02).
           03  FILLER                            PIC X(97).
           03  MIC004-DATA-AREA-SG               PIC X(8181).
      *    ---- TYPE A/B: DATA AREA = MIC003 QUEUE RECORD ----
           03  MIC004-MIC003-REC-SG REDEFINES MIC004-DATA-AREA-SG.
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

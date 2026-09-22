//*********************************************************************
//*                                                                   *
//*  MEMBER   : PATTERNS                                              *
//*  PURPOSE  : TUNED STEP PATTERNS FOR THE CARDLINK MY (MY20A2)      *
//*             BATCH.  THIS MEMBER IS A REFERENCE LIBRARY, NOT A     *
//*             RUNNABLE JOB - COPY THE PATTERN THAT MATCHES THE      *
//*             STEP BEING TUNED INTO THE TARGET MEMBER OF            *
//*             BTHJCL OR BTHPRC LIBRARY OF THE TARGET REGION.        *
//*                                                                   *
//*  EVIDENCE : ../reports/05_sort_dynalloc_candidates.csv            *
//*             ../reports/06_sort_intermediates.csv                  *
//*             ../reports/07_copy_candidates.csv                     *
//*                                                                   *
//*  RULE     : EVERY PATTERN BELOW IS ALLOCATION, BUFFERING OR STEP  *
//*             STRUCTURE ONLY.  NONE CHANGES RECORD CONTENT OR SORT  *
//*             ORDER, SO EACH ONE IS PROVABLE WITH IEBCOMPR AGAINST  *
//*             THE CURRENT PRODUCTION OUTPUT (SEE JMYBTUNE).         *
//*                                                                   *
//*********************************************************************
//*
//*====================================================================*
//* P1 - VSAM MASTER READ SEQUENTIALLY                                 *
//*      APPLIES TO CPBCRD / CPBCUS / CPBPLT / CPBKYC / KCMACC /       *
//*      EPTRANS AND EVERY OTHER KSDS A CP6 MAIN READS END TO END.     *
//*                                                                    *
//*      BEFORE: //CPBCRD  DD DSN=&ENV.CIS.BTHVSM.&VER.CPBCRD,DISP=SHR *
//*      AFTER : ADD AMP.  ACCBIAS=SO ASKS VSAM SYSTEM MANAGED         *
//*              BUFFERING FOR A SEQUENTIAL BIAS AND LETS IT PICK      *
//*              THE BUFFER COUNT; IT REPLACES HAND-TUNED BUFND AND    *
//*              SURVIVES DATASET GROWTH.  PERFORMANCE ONLY - THE      *
//*              RECORDS RETURNED ARE IDENTICAL.                       *
//*====================================================================*
//CPBCRD   DD  DSN=&ENV.CIS.BTHVSM.&VER.CPBCRD,DISP=SHR,
//             AMP=('ACCBIAS=SO')
//*
//*      WHERE THE CLUSTER IS NOT SMS EXTENDED FORMAT, SMB IS NOT
//*      ELIGIBLE AND THE BUFFERS MUST BE GIVEN EXPLICITLY INSTEAD:
//*
//CPBCUS   DD  DSN=&ENV.CIS.BTHVSM.&VER.CPBCUS,DISP=SHR,
//             AMP=('BUFND=60,BUFNI=8')
//*
//*      KEYED / RANDOM ACCESS IS THE OPPOSITE TRADE - INDEX BUFFERS
//*      MATTER, DATA BUFFERS DO NOT:
//*
//CPBPLT   DD  DSN=&ENV.CIS.BTHVSM.&VER.CPBPLT,DISP=SHR,
//             AMP=('ACCBIAS=DO,BUFNI=20,BUFND=4')
//*
//*====================================================================*
//* P2 - SORT STEP                                                     *
//*      287 OF THE 344 CAPTURED SORT MEMBERS CARRY NO DYNALL*         *
//*      CONTROL MEMBER, SO THEY RUN ON WHATEVER SORTWKNN THE MEMBER   *
//*      HAPPENS TO CODE.  ADD SORTCNTL AND A SIZE ESTIMATE.           *
//*                                                                    *
//*      FILSZ=E  IS AN *ESTIMATE*.  IF IT IS WRONG DFSORT ADJUSTS -   *
//*      IT NEVER ABENDS ON A BAD ESTIMATE, IT ONLY SIZES SORT WORK    *
//*      AND STORAGE BETTER WHEN IT IS RIGHT.                          *
//*====================================================================*
//SORT010  EXEC PGM=SORT,REGION=0M
//SYSOUT   DD  SYSOUT=*
//SORTCNTL DD  DSN=&CNTLLIB(DYNALL64),DISP=SHR
//SORTIN   DD  DSN=&ENV.CRD.BTHSEQ.&VER.RDM.CUSPLT,DISP=SHR
//SORTOUT  DD  DSN=&ENV.CRD.BTHSEQ.&VER.RDM.CUSPLT.O,
//             DISP=(NEW,CATLG,DELETE),
//             SPACE=(CYL,(200,100),RLSE),
//             DATACLAS=EXTPREF
//SYSIN    DD  *
  SORT FIELDS=(1,19,CH,A)
  OPTION FILSZ=E4000000,AVGRLEN=600
/*
//*
//*====================================================================*
//* P3 - COLLAPSE A SORT-TO-DASD-THEN-REREAD CHAIN INTO ONE PASS       *
//*      60 CAPTURED MEMBERS LAND SORT OUTPUT ON A PERMANENT .SORT /   *
//*      .SRT / .SORTED DATASET AND READ IT BACK IN A LATER STEP.      *
//*      EACH SUCH INTERMEDIATE COSTS A FULL WRITE PLUS A FULL READ.   *
//*                                                                    *
//*      BEFORE: STEP1 SORT -> MERCHFL.SORT1                           *
//*              STEP2 SORT -> MERCHFL.SORT2                           *
//*              STEP3 PGM READS BOTH                                  *
//*      AFTER : ONE DFSORT PASS WITH OUTFIL FANOUT.  THE SPLIT IS     *
//*              DONE ON THE SAME SELECTION THE TWO SORTS USED, SO     *
//*              THE TWO OUTPUTS ARE BYTE-FOR-BYTE WHAT THEY WERE.     *
//*                                                                    *
//*      KEEP THE OUTPUT DSNS IF DOWNSTREAM JOBS OR THE RERUN          *
//*      PROCEDURE REFERENCE THEM; ONLY THE EXTRA PASS IS REMOVED.     *
//*====================================================================*
//SORT020  EXEC PGM=SORT,REGION=0M
//SYSOUT   DD  SYSOUT=*
//SORTCNTL DD  DSN=&CNTLLIB(DYNALL64),DISP=SHR
//SORTIN   DD  DSN=&ENV.CRD.BTHSEQ.&VER.MERCHFL,DISP=SHR
//OUT1     DD  DSN=&ENV.CRD.BTHSEQ.&VER.MERCHFL.SORT1,
//             DISP=(NEW,CATLG,DELETE),SPACE=(CYL,(100,100),RLSE)
//OUT2     DD  DSN=&ENV.CRD.BTHSEQ.&VER.MERCHFL.SORT2,
//             DISP=(NEW,CATLG,DELETE),SPACE=(CYL,(100,100),RLSE)
//SYSIN    DD  *
  SORT FIELDS=(1,15,CH,A)
  OUTFIL FNAMES=OUT1,INCLUDE=(16,1,CH,EQ,C'M')
  OUTFIL FNAMES=OUT2,INCLUDE=(16,1,CH,EQ,C'P')
/*
//*
//*====================================================================*
//* P4 - IEBGENER -> ICEGENER                                          *
//*      ONLY 2 CAPTURED MEMBERS STILL RUN IEBGENER (THE ESTATE IS     *
//*      OTHERWISE CONVERTED - 129 MEMBERS ALREADY USE ICEGENER).      *
//*      ICEGENER IS A DROP-IN: SAME DD NAMES, SAME SYSIN, AND IT      *
//*      FALLS BACK TO IEBGENER BY ITSELF FOR ANYTHING IT CANNOT DO.   *
//*====================================================================*
//COPY010  EXEC PGM=ICEGENER
//SYSPRINT DD  SYSOUT=*
//SYSUT1   DD  DSN=&ENV.CRD.BTHSEQ.&VER.EDCTOCP,DISP=SHR
//SYSUT2   DD  DSN=&ENV.CRD.BTHSEQ.&VER.EDCTOCP.CPY,
//             DISP=(NEW,CATLG,DELETE),SPACE=(CYL,(50,100),RLSE)
//SYSIN    DD  DUMMY
//*
//*====================================================================*
//* P5 - LARGE SEQUENTIAL EXTRACT                                      *
//*      THE CP6 EXTRACTS THAT FEED SAS / BDW / EIS WRITE MILLIONS OF  *
//*      RECORDS THROUGH QSAM.  THREE CHANGES, ALL PERFORMANCE ONLY:   *
//*        - BUFNO=64     DEEPER READ-AHEAD / WRITE-BEHIND             *
//*        - BLKSIZE=0    SYSTEM DETERMINED BLOCK SIZE (HALF TRACK)    *
//*        - DATACLAS     EXTENDED FORMAT + STRIPING WHERE THE         *
//*                       STORAGE GROUP SUPPORTS IT                    *
//*      RLSE RETURNS THE OVER-ALLOCATION INSTEAD OF HOLDING IT FOR    *
//*      THE REST OF THE CYCLE.                                        *
//*====================================================================*
//EXTRACT  DD  DSN=&ENV.CIS.BTHSEQ.&VER.SAS.GLFSAHCI.FTP,
//             DISP=(NEW,CATLG,DELETE),
//             SPACE=(CYL,(500,200),RLSE),
//             DATACLAS=EXTPREF,
//             DCB=(RECFM=FB,LRECL=600,BLKSIZE=0,BUFNO=64)
//*
//*====================================================================*
//* P6 - PARTITION A SINGLE-THREADED LONG RUNNER                       *
//*      FOR THE FOUR JOBS THAT ARE LONGER THAN THE REST OF THEIR      *
//*      PLAN'S CHAIN PUT TOGETHER (SEE 03_CRITICAL_PATH.CSV).         *
//*      THE MASTER IS SPLIT BY KEY RANGE AND THE RANGES RUN AS        *
//*      SEPARATE JOBS IN THE SAME OPC PLAN, THEN MERGE.               *
//*                                                                    *
//*      THIS IS THE ONLY PATTERN HERE THAT NEEDS AN OPC CHANGE AND    *
//*      AN APPLICATION-OWNER DECISION: IT IS SAFE ONLY WHERE THE      *
//*      PROGRAM CARRIES NO CROSS-ACCOUNT STATE AND NO CONTROL TOTAL   *
//*      THAT SPANS THE WHOLE FILE.  CONFIRM BEFORE USE.               *
//*====================================================================*
//SPLIT010 EXEC PGM=SORT,REGION=0M
//SYSOUT   DD  SYSOUT=*
//SORTCNTL DD  DSN=&CNTLLIB(DYNALL64),DISP=SHR
//SORTIN   DD  DSN=&ENV.CRD.BTHSEQ.&VER.RDM.CUSPLT,DISP=SHR
//PART1    DD  DSN=&ENV.CRD.BTHSEQ.&VER.RDM.CUSPLT.P1,
//             DISP=(NEW,CATLG,DELETE),SPACE=(CYL,(200,100),RLSE)
//PART2    DD  DSN=&ENV.CRD.BTHSEQ.&VER.RDM.CUSPLT.P2,
//             DISP=(NEW,CATLG,DELETE),SPACE=(CYL,(200,100),RLSE)
//PART3    DD  DSN=&ENV.CRD.BTHSEQ.&VER.RDM.CUSPLT.P3,
//             DISP=(NEW,CATLG,DELETE),SPACE=(CYL,(200,100),RLSE)
//PART4    DD  DSN=&ENV.CRD.BTHSEQ.&VER.RDM.CUSPLT.P4,
//             DISP=(NEW,CATLG,DELETE),SPACE=(CYL,(200,100),RLSE)
//SYSIN    DD  *
  SORT FIELDS=COPY
  OUTFIL FNAMES=PART1,INCLUDE=(1,1,CH,LE,C'3')
  OUTFIL FNAMES=PART2,INCLUDE=(1,1,CH,GT,C'3',AND,1,1,CH,LE,C'5')
  OUTFIL FNAMES=PART3,INCLUDE=(1,1,CH,GT,C'5',AND,1,1,CH,LE,C'7')
  OUTFIL FNAMES=PART4,INCLUDE=(1,1,CH,GT,C'7')
/*
//*
//*====================================================================*
//* P7 - BULK COPY: IDCAMS REPRO -> DFSORT                             *
//*      IDCAMS IS THE RIGHT TOOL FOR DEFINE / DELETE / LISTCAT AND    *
//*      FOR LOADING A KSDS.  FOR A STRAIGHT SEQUENTIAL BULK COPY      *
//*      DFSORT IS THE FASTER PATH BECAUSE IT BLOCKS AND BUFFERS THE   *
//*      TRANSFER ITSELF.  388 CAPTURED MEMBERS RUN IDCAMS; ONLY THE   *
//*      PLAIN PS-TO-PS REPRO STEPS ARE CANDIDATES - LEAVE VSAM        *
//*      LOADS, DEFINES AND DELETES ON IDCAMS.                         *
//*====================================================================*
//COPY020  EXEC PGM=SORT,REGION=0M
//SYSOUT   DD  SYSOUT=*
//SORTCNTL DD  DSN=&CNTLLIB(DYNALL64),DISP=SHR
//SORTIN   DD  DSN=&ENV.CRD.BTHSEQ.&VER.QMEPST,DISP=SHR
//SORTOUT  DD  DSN=&ENV.CRD.BTHSEQ.&VER.QMEPST.BKP,
//             DISP=(NEW,CATLG,DELETE),SPACE=(CYL,(300,100),RLSE)
//SYSIN    DD  *
  SORT FIELDS=COPY
/*

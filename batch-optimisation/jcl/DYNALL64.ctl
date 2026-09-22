*--------------------------------------------------------------------*
*                                                                    *
*  MEMBER   : DYNALL64                                               *
*  LIBRARY  : PRDCRD.BTHCTL.MY20A2      (&CNTLLIB)                   *
*  LCM TYPE : CTL  (control card - no compile, no genbase)           *
*                                                                    *
*  PURPOSE  : STANDARD DFSORT OPTION CARD FOR THE MY BATCH.          *
*             COMPANION TO THE EXISTING DYNALL32 MEMBER, SIZED FOR   *
*             THE LARGE MASTER-FILE SORTS (CPBCRD / CPBCUS / CPBPLT  *
*             / KCMACC / QMHST) THAT DOMINATE THE A7 CRITICAL PATH.  *
*                                                                    *
*  USAGE    : //DFSPARM  DD DSN=&CNTLLIB(DYNALL64),DISP=SHR          *
*             THE STEP'S OWN SYSIN KEEPS ITS SORT / INCLUDE /        *
*             INREC / OUTREC CARDS UNCHANGED.                        *
*                                                                    *
*  RELATED  : THE ESTATE ALREADY HAS TWO FAMILIES OF SORT PARM       *
*             MEMBERS IN &CNTLLIB, BOTH READ THROUGH DFSPARM:        *
*               DYNALL<N>  - SETS THE SORT WORK COUNT ONLY           *
*               ICPK<NNNN> - FILSZ ESTIMATE PLUS DYNALLOC, WHERE     *
*                            NNNN SCALES THE ESTIMATE.  ICPK5000 IS  *
*                            OPTION FILSZ=E5000000,DYNALLOC=(DISK,32)*
*             WHERE A STEP'S RECORD VOLUME IS KNOWN, PREFER THE      *
*             MATCHING ICPK MEMBER - A CORRECT FILSZ IS WORTH MORE   *
*             THAN EXTRA SORT WORK DATASETS.  USE DYNALL64 WHEN THE  *
*             VOLUME IS UNKNOWN OR VARIES WIDELY RUN TO RUN.         *
*                                                                    *
*  EVERY OPTION BELOW IS ALLOCATION OR STORAGE ONLY.  NONE OF THEM   *
*  CHANGES THE RECORD CONTENT OR THE ORDER OF THE SORTED OUTPUT.     *
*  DO NOT ADD  NOEQUALS  OR  VLSHRT  TO THIS MEMBER - BOTH ALTER     *
*  RESULTS AND MUST BE DECIDED PER JOB BY THE APPLICATION OWNER.     *
*                                                                    *
*--------------------------------------------------------------------*
*                                                                    *
*  DYNALLOC=(DISK,64)   DFSORT ALLOCATES ITS OWN SORT WORK ACROSS    *
*                       64 DATASETS INSTEAD OF THE FIXED SORTWKNN    *
*                       DD CARDS.  REMOVES THE "SORT CAPACITY        *
*                       EXCEEDED" (ICE046A) RERUNS ON VOLUME GROWTH  *
*                       AND SPREADS I/O OVER MORE VOLUMES.  DISK IS  *
*                       THE ESTATE'S UNIT NAME - ICPK5000 AND        *
*                       DYNALL32 BOTH USE IT.                        *
*                                                                    *
*  MAINSIZE=MAX         LET DFSORT TAKE THE REGION IT IS GIVEN.      *
*                       REQUIRES REGION=0M ON THE EXEC OR JOB CARD.  *
*                                                                    *
*  HIPRMAX=OPTIMAL      USE HIPERSPACE FOR INTERMEDIATE MERGE DATA   *
*                       WHEN CENTRAL STORAGE ALLOWS, WHICH REMOVES   *
*                       THE SORT WORK I/O ALTOGETHER ON MID-SIZED    *
*                       SORTS.  DFSORT BACKS OFF AUTOMATICALLY WHEN  *
*                       THE SYSTEM IS SHORT OF STORAGE.              *
*                                                                    *
*  DSA=128              CEILING IN MB FOR DYNAMIC STORAGE ADJUSTMENT *
*                       WHEN MEMORY OBJECT SORTING IS ELIGIBLE.      *
*                                                                    *
*--------------------------------------------------------------------*
  OPTION DYNALLOC=(DISK,64),MAINSIZE=MAX,HIPRMAX=OPTIMAL,DSA=128

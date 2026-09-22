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
*  USAGE    : //SORTCNTL DD DSN=&CNTLLIB(DYNALL64),DISP=SHR          *
*             THE STEP'S OWN SYSIN KEEPS ITS SORT / INCLUDE /        *
*             INREC / OUTREC CARDS UNCHANGED.                        *
*                                                                    *
*  EVERY OPTION BELOW IS ALLOCATION OR STORAGE ONLY.  NONE OF THEM   *
*  CHANGES THE RECORD CONTENT OR THE ORDER OF THE SORTED OUTPUT.     *
*  DO NOT ADD  NOEQUALS  OR  VLSHRT  TO THIS MEMBER - BOTH ALTER     *
*  RESULTS AND MUST BE DECIDED PER JOB BY THE APPLICATION OWNER.     *
*                                                                    *
*--------------------------------------------------------------------*
*                                                                    *
*  DYNALLOC=(SYSDA,64)  DFSORT ALLOCATES ITS OWN SORT WORK ACROSS    *
*                       64 DATASETS INSTEAD OF THE FIXED SORTWKNN    *
*                       DD CARDS.  REMOVES THE "SORT CAPACITY        *
*                       EXCEEDED" (ICE046A) RERUNS ON VOLUME GROWTH  *
*                       AND SPREADS I/O OVER MORE VOLUMES.           *
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
  OPTION DYNALLOC=(SYSDA,64),MAINSIZE=MAX,HIPRMAX=OPTIMAL,DSA=128

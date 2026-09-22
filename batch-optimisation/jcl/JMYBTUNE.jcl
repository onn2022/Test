//JMYBTUNE JOB (ACCT),'MY BATCH TUNE VERIFY',
//             CLASS=A,
//             MSGCLASS=X,
//             MSGLEVEL=(1,1),
//             NOTIFY=&SYSUID,
//             REGION=0M
//*********************************************************************
//*                                                                   *
//*  JOB NAME : JMYBTUNE                                              *
//*  PURPOSE  : PROVE THAT A TUNED CARDLINK MY BATCH STEP PRODUCES    *
//*             BYTE-FOR-BYTE THE SAME OUTPUT AS THE UNTUNED STEP.    *
//*                                                                   *
//*             RUN THIS FOR EVERY MEMBER TOUCHED BY THE TUNING       *
//*             CHANGE.  IT IS THE EVIDENCE FOR IMPACT ANALYSIS       *
//*             CHECKLIST ITEM A2 (JCL TESTED WITH AT LEAST ONE       *
//*             SUCCESSFUL END-TO-END RUN) AND FOR THE CAB PACK.      *
//*             RUN IT TWICE - SECOND-RUN BEHAVIOUR IS WHERE GDG      *
//*             AND CATALOG DEFECTS APPEAR.                           *
//*                                                                   *
//*  WHERE    : THIS MEMBER IS HELD IN PRODUCTION FORM.  EXECUTE IT   *
//*             IN UAT (MY20A6) ON THE JCL CONVERTER OUTPUT, PER IA   *
//*             ITEM A1.  THE PRODUCTION FORM STAYS THE MASTER AND    *
//*             THE CONVERTED TEST VERSION IS NEVER PROMOTED.         *
//*                                                                   *
//*  SAFETY   : EVERY STEP IS READ-ONLY EXCEPT FOR ITS OWN WORK       *
//*             DATASETS.  NO MASTER FILE IS OPENED FOR OUTPUT AND    *
//*             THE JOB CAN BE CANCELLED AT ANY POINT.                *
//*                                                                   *
//*  USAGE    : 1. SET TGTJOB TO THE JCL MEMBER UNDER TEST.           *
//*             2. BASESFX / TUNESFX NAME THE TWO OUTPUTS TO BE       *
//*                COMPARED.  THE BASELINE MUST BE TAKEN BEFORE THE   *
//*                TUNING CHANGE IS APPLIED.                          *
//*             3. SUBMIT.  STEP CMPOUT MUST END RC=00.  ANY OTHER    *
//*                RETURN CODE MEANS THE TUNING CHANGED THE DATA -    *
//*                BACK IT OUT, DO NOT RAISE THE RFC.                 *
//*                                                                   *
//*********************************************************************
//*
//         JCLLIB ORDER=(PRDCRD.BTHPRC.MY20A2)  PROD MASTER: THE JCL
//*                                             CONVERTER SWAPS THIS
//*                                             FOR THE UAT LIBRARY.
//         INCLUDE MEMBER=JOBLIB
//         INCLUDE MEMBER=COMMVAR
//*
//         SET TGTJOB=JCP1028U           JCL MEMBER UNDER TEST
//         SET BASESFX=TUNE.BASELINE     OUTPUT OF THE UNTUNED RUN
//         SET TUNESFX=TUNE.TUNED        OUTPUT OF THE TUNED RUN
//*
//*--------------------------------------------------------------------*
//* STEP 1 - SHOW THE SORT OPTIONS THAT WILL BE IN FORCE               *
//*          DFSORT ECHOES THE MERGED OPTION SET TO SYSOUT, SO THE     *
//*          SPOOL PROVES WHICH CONTROL MEMBER WAS PICKED UP.          *
//*--------------------------------------------------------------------*
//SHOWOPT  EXEC PGM=SORT,REGION=0M
//SYSOUT   DD   SYSOUT=*
//SORTCNTL DD   DSN=&CNTLLIB(DYNALL64),DISP=SHR
//SORTIN   DD   DUMMY,DCB=(RECFM=FB,LRECL=80,BLKSIZE=800)
//SORTOUT  DD   DUMMY,DCB=(RECFM=FB,LRECL=80,BLKSIZE=800)
//SYSIN    DD   *
  SORT FIELDS=COPY
  OPTION MSGPRT=ALL
/*
//*
//*--------------------------------------------------------------------*
//* STEP 2 - COUNT BOTH FILES BEFORE COMPARING                         *
//*          A RECORD-COUNT DIFFERENCE IS EASIER TO READ IN THE SPOOL  *
//*          THAN THE IEBCOMPR "END OF FILE ON ONE INPUT" MESSAGE.     *
//*--------------------------------------------------------------------*
//CNTBASE  EXEC PGM=ICETOOL
//TOOLMSG  DD   SYSOUT=*
//DFSMSG   DD   SYSOUT=*
//BASE     DD   DSN=&ENV.CRD.WRKSEQ.&VER.&BASESFX,DISP=SHR
//TUNED    DD   DSN=&ENV.CRD.WRKSEQ.&VER.&TUNESFX,DISP=SHR
//TOOLIN   DD   *
  COUNT FROM(BASE)  WRITE(TOOLMSG) TEXT('BASELINE RECORD COUNT')
  COUNT FROM(TUNED) WRITE(TOOLMSG) TEXT('TUNED    RECORD COUNT')
/*
//*
//*--------------------------------------------------------------------*
//* STEP 3 - THE ACTUAL EQUIVALENCE TEST                               *
//*          RC=00 IS THE ONLY ACCEPTABLE RESULT.                      *
//*--------------------------------------------------------------------*
//CMPOUT   EXEC PGM=IEBCOMPR,COND=(0,NE,CNTBASE)
//SYSPRINT DD   SYSOUT=*
//SYSUT1   DD   DSN=&ENV.CRD.WRKSEQ.&VER.&BASESFX,DISP=SHR
//SYSUT2   DD   DSN=&ENV.CRD.WRKSEQ.&VER.&TUNESFX,DISP=SHR
//SYSIN    DD   *
  COMPARE TYPORG=PS
/*
//*
//*--------------------------------------------------------------------*
//* STEP 4 - LIST THE MEMBER AS RUN, FOR THE SOURCE COMPARE PACK       *
//*--------------------------------------------------------------------*
//LISTJCL  EXEC PGM=IEBPTPCH,COND=EVEN
//SYSPRINT DD   SYSOUT=*
//SYSUT1   DD   DSN=&ENV.CRD.BTHJCL.&VER1(&TGTJOB),DISP=SHR
//SYSUT2   DD   SYSOUT=*
//SYSIN    DD   *
  PRINT TYPORG=PS
/*

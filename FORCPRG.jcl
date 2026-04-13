//FORCPRG  JOB (ACCT),'FORCE PURGE CICS TASK',
//             CLASS=A,
//             MSGCLASS=X,
//             MSGLEVEL=(1,1),
//             NOTIFY=&SYSUID,
//             REGION=0M
//*********************************************************************
//*                                                                   *
//*  JOB NAME : FORCPRG                                               *
//*  PURPOSE  : FORCE PURGE A HUNG / LOOPING TASK IN A CICS REGION    *
//*             BY ISSUING THE CEMT SET TASK FORCEPURGE COMMAND       *
//*             AS AN MVS MODIFY (F) CONSOLE COMMAND THROUGH TSO      *
//*             USING THE IKJEFT01 TERMINAL MONITOR PROGRAM.          *
//*                                                                   *
//*  USAGE    : 1. UPDATE THE SYMBOLIC PARAMETERS BELOW:              *
//*               CICSRGN  = CICS REGION JOBNAME / STARTED TASK NAME  *
//*               TASKNUM  = CICS TASK NUMBER TO BE FORCE PURGED      *
//*             2. SUBMIT THE JOB.                                    *
//*                                                                   *
//*  WARNING  : FORCEPURGE CAN LEAVE RESOURCES IN AN INCONSISTENT     *
//*             STATE. ONLY USE WHEN A NORMAL "PURGE" HAS FAILED      *
//*             AND THE TASK MUST BE REMOVED FROM THE REGION.         *
//*                                                                   *
//*********************************************************************
//*
//         SET CICSRGN=CICSPROD          CICS REGION JOBNAME
//         SET TASKNUM=0000000           CICS TASK NUMBER (7 DIGITS)
//*
//*--------------------------------------------------------------------*
//* STEP 1 - DISPLAY THE TASK BEFORE ATTEMPTING THE PURGE              *
//*--------------------------------------------------------------------*
//INQTASK  EXEC PGM=IKJEFT01,DYNAMNBR=20
//SYSTSPRT DD   SYSOUT=*
//SYSTSIN  DD   *,SYMBOLS=JCLONLY
  CONSOLE ACTIVATE
  CONSOLE SYSCMD(F &CICSRGN,CEMT INQUIRE TASK(&TASKNUM))
  CONSOLE DEACTIVATE
/*
//*
//*--------------------------------------------------------------------*
//* STEP 2 - TRY A NORMAL PURGE FIRST (RECOMMENDED PRACTICE)           *
//*          IF THE TASK ENDS, STEP 3 IS NOT REQUIRED.                 *
//*--------------------------------------------------------------------*
//PURGE    EXEC PGM=IKJEFT01,DYNAMNBR=20
//SYSTSPRT DD   SYSOUT=*
//SYSTSIN  DD   *,SYMBOLS=JCLONLY
  CONSOLE ACTIVATE
  CONSOLE SYSCMD(F &CICSRGN,CEMT SET TASK(&TASKNUM) PURGE)
  CONSOLE DEACTIVATE
/*
//*
//*--------------------------------------------------------------------*
//* STEP 3 - FORCE PURGE THE TASK IF THE NORMAL PURGE FAILED           *
//*--------------------------------------------------------------------*
//FORCPRG  EXEC PGM=IKJEFT01,DYNAMNBR=20,COND=EVEN
//SYSTSPRT DD   SYSOUT=*
//SYSTSIN  DD   *,SYMBOLS=JCLONLY
  CONSOLE ACTIVATE
  CONSOLE SYSCMD(F &CICSRGN,CEMT SET TASK(&TASKNUM) FORCEPURGE)
  CONSOLE DEACTIVATE
/*
//*
//*--------------------------------------------------------------------*
//* STEP 4 - VERIFY THAT THE TASK HAS BEEN REMOVED                     *
//*--------------------------------------------------------------------*
//VERIFY   EXEC PGM=IKJEFT01,DYNAMNBR=20,COND=EVEN
//SYSTSPRT DD   SYSOUT=*
//SYSTSIN  DD   *,SYMBOLS=JCLONLY
  CONSOLE ACTIVATE
  CONSOLE SYSCMD(F &CICSRGN,CEMT INQUIRE TASK(&TASKNUM))
  CONSOLE DEACTIVATE
/*
//

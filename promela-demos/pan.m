#define rand	pan_rand
#define pthread_equal(a,b)	((a)==(b))
#if defined(HAS_CODE) && defined(VERBOSE)
	#ifdef BFS_PAR
		bfs_printf("Pr: %d Tr: %d\n", II, t->forw);
	#else
		cpu_printf("Pr: %d Tr: %d\n", II, t->forw);
	#endif
#endif
	switch (t->forw) {
	default: Uerror("bad forward move");
	case 0:	/* if without executable clauses */
		continue;
	case 1: /* generic 'goto' or 'skip' */
		IfNotBlocked
		_m = 3; goto P999;
	case 2: /* generic 'else' */
		IfNotBlocked
		if (trpt->o_pm&1) continue;
		_m = 3; goto P999;

		 /* PROC :init: */
	case 3: // STATE 1 - loop-prob.pml:33 - [(run driver(1))] (0:0:0 - 1)
		IfNotBlocked
		reached[2][1] = 1;
		if (!(addproc(II, 1, 1, 1)))
			continue;
		_m = 3; goto P999; /* 0 */
	case 4: // STATE 2 - loop-prob.pml:34 - [-end-] (0:0:0 - 1)
		IfNotBlocked
		reached[2][2] = 1;
		if (!delproc(1, II)) continue;
		_m = 3; goto P999; /* 0 */

		 /* PROC driver */
	case 5: // STATE 1 - loop-prob.pml:26 - [i = 1] (0:0:1 - 1)
		IfNotBlocked
		reached[1][1] = 1;
		(trpt+1)->bup.oval = ((P1 *)_this)->i;
		((P1 *)_this)->i = 1;
#ifdef VAR_RANGES
		logval("driver:i", ((P1 *)_this)->i);
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 6: // STATE 2 - loop-prob.pml:26 - [((i<=nproc))] (0:0:0 - 1)
		IfNotBlocked
		reached[1][2] = 1;
		if (!((((P1 *)_this)->i<=((P1 *)_this)->nproc)))
			continue;
		_m = 3; goto P999; /* 0 */
	case 7: // STATE 3 - loop-prob.pml:27 - [(run worker())] (0:0:0 - 1)
		IfNotBlocked
		reached[1][3] = 1;
		if (!(addproc(II, 1, 0, 0)))
			continue;
		_m = 3; goto P999; /* 0 */
	case 8: // STATE 4 - loop-prob.pml:26 - [i = (i+1)] (0:0:1 - 1)
		IfNotBlocked
		reached[1][4] = 1;
		(trpt+1)->bup.oval = ((P1 *)_this)->i;
		((P1 *)_this)->i = (((P1 *)_this)->i+1);
#ifdef VAR_RANGES
		logval("driver:i", ((P1 *)_this)->i);
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 9: // STATE 10 - loop-prob.pml:29 - [-end-] (0:0:0 - 3)
		IfNotBlocked
		reached[1][10] = 1;
		if (!delproc(1, II)) continue;
		_m = 3; goto P999; /* 0 */

		 /* PROC worker */
	case 10: // STATE 1 - loop-prob.pml:5 - [open_flags = 65] (0:0:2 - 1)
		IfNotBlocked
		reached[0][1] = 1;
		(trpt+1)->bup.ovals = grab_ints(2);
		(trpt+1)->bup.ovals[0] = ((P0 *)_this)->open_flags;
		((P0 *)_this)->open_flags = 65;
#ifdef VAR_RANGES
		logval("worker:open_flags", ((P0 *)_this)->open_flags);
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 11: // STATE 2 - loop-prob.pml:6 - [open_flags = 193] (0:0:2 - 1)
		IfNotBlocked
		reached[0][2] = 1;
		(trpt+1)->bup.ovals = grab_ints(2);
		(trpt+1)->bup.ovals[0] = ((P0 *)_this)->open_flags;
		((P0 *)_this)->open_flags = 193;
#ifdef VAR_RANGES
		logval("worker:open_flags", ((P0 *)_this)->open_flags);
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 12: // STATE 3 - loop-prob.pml:7 - [open_flags = 577] (0:0:2 - 1)
		IfNotBlocked
		reached[0][3] = 1;
		(trpt+1)->bup.ovals = grab_ints(2);
		(trpt+1)->bup.ovals[0] = ((P0 *)_this)->open_flags;
		((P0 *)_this)->open_flags = 577;
#ifdef VAR_RANGES
		logval("worker:open_flags", ((P0 *)_this)->open_flags);
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 13: // STATE 4 - loop-prob.pml:8 - [open_flags = 16449] (0:0:2 - 1)
		IfNotBlocked
		reached[0][4] = 1;
		(trpt+1)->bup.ovals = grab_ints(2);
		(trpt+1)->bup.ovals[0] = ((P0 *)_this)->open_flags;
		((P0 *)_this)->open_flags = 16449;
#ifdef VAR_RANGES
		logval("worker:open_flags", ((P0 *)_this)->open_flags);
#endif
		;
		_m = 3; goto P999; /* 0 */
	case 14: // STATE 9 - loop-prob.pml:18 - [{c_code1}] (0:0:0 - 1)
		IfNotBlocked
		reached[0][9] = 1;
		/* c_code1 */
		{ 
		sv_save(); printf("open flag: %d \n", Pworker->open_flags);  }

#if defined(C_States) && (HAS_TRACK==1)
		c_update((uchar *) &(now.c_state[0]));
#endif
;
		_m = 3; goto P999; /* 0 */
	case 15: // STATE 14 - loop-prob.pml:21 - [-end-] (0:0:0 - 1)
		IfNotBlocked
		reached[0][14] = 1;
		if (!delproc(1, II)) continue;
		_m = 3; goto P999; /* 0 */
	case  _T5:	/* np_ */
		if (!((!(trpt->o_pm&4) && !(trpt->tau&128))))
			continue;
		/* else fall through */
	case  _T2:	/* true */
		_m = 3; goto P999;
#undef rand
	}


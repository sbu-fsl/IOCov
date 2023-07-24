	switch (t->back) {
	default: Uerror("bad return move");
	case  0: goto R999; /* nothing to undo */

		 /* PROC :init: */

	case 3: // STATE 1
		;
		;
		delproc(0, now._nr_pr-1);
		;
		goto R999;

	case 4: // STATE 2
		;
		p_restor(II);
		;
		;
		goto R999;

		 /* PROC driver */

	case 5: // STATE 1
		;
		((P1 *)_this)->i = trpt->bup.oval;
		;
		goto R999;
;
		;
		
	case 7: // STATE 3
		;
		;
		delproc(0, now._nr_pr-1);
		;
		goto R999;

	case 8: // STATE 4
		;
		((P1 *)_this)->i = trpt->bup.oval;
		;
		goto R999;

	case 9: // STATE 10
		;
		p_restor(II);
		;
		;
		goto R999;

		 /* PROC worker */

	case 10: // STATE 1
		;
		((P0 *)_this)->open_flags = trpt->bup.ovals[0];
		;
		ungrab_ints(trpt->bup.ovals, 2);
		goto R999;

	case 11: // STATE 2
		;
		((P0 *)_this)->open_flags = trpt->bup.ovals[0];
		;
		ungrab_ints(trpt->bup.ovals, 2);
		goto R999;

	case 12: // STATE 3
		;
		((P0 *)_this)->open_flags = trpt->bup.ovals[0];
		;
		ungrab_ints(trpt->bup.ovals, 2);
		goto R999;

	case 13: // STATE 4
		;
		((P0 *)_this)->open_flags = trpt->bup.ovals[0];
		;
		ungrab_ints(trpt->bup.ovals, 2);
		goto R999;

	case 14: // STATE 9
		;
		sv_restor();
;
		;
		goto R999;

	case 15: // STATE 14
		;
		p_restor(II);
		;
		;
		goto R999;
	}


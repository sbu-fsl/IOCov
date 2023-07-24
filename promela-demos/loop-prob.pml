/* Select values with probabilities */

inline pick_open_flags(value) {
	if
		:: value = 65;
		:: value = 193;
		:: value = 577;
		:: value = 16449;
	fi
}

proctype worker()
{
    int open_flags;
    do
    :: pick_open_flags(open_flags);
       atomic {
        c_code { printf("open flag: %d \n", Pworker->open_flags); };
       };
    od 
}

proctype driver(int nproc)
{
    int i;
    for (i : 1 .. nproc) {
        run worker();
    }
}

init
{
    run driver(1);
}

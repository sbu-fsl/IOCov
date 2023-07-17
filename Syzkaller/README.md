# Syzkaller Parsing

## Workflow

1. First of all, we need to have a dedicated directory to contain ONLY 
   the input webpages (with input syscalls) from Syzkaller.  To do so,
   we can do `mkdir only-inputs && cd 127.0.0.1:56741` and `cp *input* ../only-inputs/`
2. With the `only-inputs` directory, change the `input_dir` field in 
   the `syscall_parse.py` script to the exact `only-inputs` for the 
   Syzkaller input webpages we want to parse.



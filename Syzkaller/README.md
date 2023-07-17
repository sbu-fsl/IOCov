# Syzkaller Input Coverage

## Collect Syzkaller Input Coverage

1. `wget --mirror --page-requisites --convert-link --no-clobber --no-parent http://127.0.0.1:56741`


## Syzkaller Parsing Workflow

1. First of all, we need to have a dedicated directory to contain ONLY 
   the input webpages (with input syscalls) from Syzkaller.  To do so,
   we can do `mkdir only-inputs && cd 127.0.0.1:56741` and `cp *input* ../only-inputs/`
2. With the `only-inputs` directory, change the `input_dir` field in 
   the `syscall_parse.py` script to the exact `only-inputs` for the 
   Syzkaller input webpages we want to parse.  Make sure the pathname 
   follows the rules so that the suffix is extracted properly.  Then, 
   run the `syscall_parse.py` script by following command to obtain 
   the `raw-syzkaller-syscalls-*.xlsx` file:

```bash
python3 syscall_parse.py
```

3. Change the `name_suffix` and `xlsx_file` fields in the `build_json.py`
   accordingly.  Then run the `build_json.py` by:

```bash
python3 build_json.py
```

4. Copy the `input_cov_syzkaller_*.pkl` files to `../src`

5. Plot the Syzkaller input/output coverage by IOCov plotter, and the 
   document is at [IOCov README](../src/README.md).

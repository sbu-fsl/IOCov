## MCFS Input Coverage

### Calculate IOCov accuracy by MCFS logs

The accuracy of IOCov's input/output coverage is computed by MCFS, which is a 
model-checking-based syscall driver and checker to save all the syscalls 
for testing to logs.  Therefore, we compare the number of syscalls from 
both MCFS logs and IOCov to find its accuracy.  We don't go deeper into 
each input or output because the accuracy calculation would be much 
more complex in this way.

The script to compute IOCov accuracy is `fig-analyzer-mcfs-precision.py`, 
which requires a `sequence-*.log` file (e.g., `sequence-pan-20230311-005751-2523268.log`)
and the pickle file from the same MCFS experiment as the sequence log (e.g., `input_cov_mcfs_10m.pkl`).

### MCFS Log Syscall Parser

The `parser-mcfs-log-input.py` script is the file to compute input coverage 
for MCFS based its logs.  

First, ensure that we have the `sequence*.log` file in the current directory (`./MCFS`),
which could also be multiple sequence log files.  Before running `parser-mcfs-log-input.py`,
we need to edit the `name_suffix` and `seq_log` to the corresponding MCFS experiments.  
Then, run `parser-mcfs-log-input.py` to parse MCFS logs and by:

```bash
python3 parser-mcfs-log-input.py
```

Finally, we plot the Syzkaller input coverage by IOCov plotter, and the 
document is at [IOCov README](../src/README.md).

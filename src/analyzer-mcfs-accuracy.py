#!/usr/bin/env python3

from constants import *
from analyzerutils import *

# MCFS may contain many sequence files, so we need to analyze them all
mcfs_seqs = ['sequence-pan-20230302-204700-182406.log']

mcfs_pkl = 'input_cov_mcfs_10m.pkl'
mcfs_iocov_input_cnt = get_syscall_count_from_pkl(mcfs_pkl)

mcfs_input_cnt = {}
for sc in INPUT_SYSCALLS.keys():
    mcfs_input_cnt[sc] = 0

for seq_path in mcfs_seqs:
    with open(seq_path) as fp:
        all_lines = fp.readlines()
        for line in all_lines:
            sc_name = line.split(',')[0]
            if sc_name in MCFS_SYSCALLS.keys():
                for each_sc in MCFS_SYSCALLS[sc_name]:
                    mcfs_input_cnt[each_sc] += 1

print('mcfs_input_cnt: ', mcfs_input_cnt)
print('mcfs_iocov_input_cnt: ', mcfs_iocov_input_cnt)

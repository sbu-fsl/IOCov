#!/usr/bin/env python3

from constants import *
from analyzerutils import *

# MCFS may contain many sequence files, so we need to analyze them all
mcfs_seqs = ['sequence-pan-20230311-005751-2523268.log']

mcfs_pkl = 'input_cov_xattr_mcfs_10m.pkl'
iocov_mcfs_input_cnt = get_syscall_count_from_pkl(mcfs_pkl)

mcfs_log_input_cnt = {}
for sc in INPUT_SYSCALLS.keys():
    mcfs_log_input_cnt[sc] = 0

for seq_path in mcfs_seqs:
    with open(seq_path) as fp:
        all_lines = fp.readlines()
        for line in all_lines:
            sc_name = line.split(',')[0]
            if sc_name in MCFS_SYSCALLS.keys():
                for each_sc in MCFS_SYSCALLS[sc_name]:
                    mcfs_log_input_cnt[each_sc] += 1

print('mcfs_log_input_cnt: ', mcfs_log_input_cnt)
print('iocov_mcfs_input_cnt: ', iocov_mcfs_input_cnt)

iocov_mcfs_precision = {}

for sc in INPUT_SYSCALLS.keys():
    if mcfs_log_input_cnt[sc] != 0:
        iocov_mcfs_precision[sc] = str((1 - abs(mcfs_log_input_cnt[sc] - iocov_mcfs_input_cnt[sc]) / mcfs_log_input_cnt[sc]) * 100 ) + ' %'

print('iocov_mcfs_precision: ', iocov_mcfs_precision)

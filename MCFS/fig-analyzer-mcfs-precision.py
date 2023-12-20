#!/usr/bin/env python3

#
# Copyright (c) 2020-2024 Yifei Liu
# Copyright (c) 2020-2024 Erez Zadok
# Copyright (c) 2020-2024 Stony Brook University
# Copyright (c) 2020-2024 The Research Foundation of SUNY
#
# You can redistribute it and/or modify it under the terms of the Apache License, 
# Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).
#

from constants import *
from analyzerutils import *

# MCFS may contain many sequence files, so we need to analyze them all
mcfs_seqs = ['sequence-pan-20230311-005751-2523268.log']

mcfs_pkl = 'input_cov_mcfs_10m.pkl'
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

fig3_iocov_mcfs_precision = {}
fig3_iocov_mcfs_error_ratio = {}

for sc in INPUT_SYSCALLS.keys():
    if mcfs_log_input_cnt[sc] != 0:
        fig3_iocov_mcfs_precision[sc] = (1 - abs(mcfs_log_input_cnt[sc] - iocov_mcfs_input_cnt[sc]) / mcfs_log_input_cnt[sc]) * 100
        fig3_iocov_mcfs_error_ratio[sc] = (abs(mcfs_log_input_cnt[sc] - iocov_mcfs_input_cnt[sc]) / mcfs_log_input_cnt[sc]) * 100

print('fig3_iocov_mcfs_precision: ', fig3_iocov_mcfs_precision)

with open('fig3_iocov_mcfs_precision.pkl', 'wb') as f:
    pickle.dump(fig3_iocov_mcfs_precision, f)

print('fig3_iocov_mcfs_error_ratio: ', fig3_iocov_mcfs_error_ratio)

print('Avg fig3_iocov_mcfs_error_ratio: ', sum(fig3_iocov_mcfs_error_ratio.values()) / len(fig3_iocov_mcfs_error_ratio))

print('fig3_iocov_mcfs_precision dumped!')

#!/usr/bin/env python3

from constants import *

mcfs_seqs = ['/mcfs2/LTTng-xfstests-2022-1211/nfs4mc/fs-state/sequence-pan-20230301-180631-510120.log']

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

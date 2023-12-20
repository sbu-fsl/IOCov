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

import os
import fnmatch
import pickle
import csv
import sys
sys.path.insert(1, '../src')
from constants import ALL_OPEN_FLAGS

need_search = True
print_all = False

# All the open flags (directly from ../src/constants.py)
# ALL_OPEN_FLAGS: all open flags 21 in a list
# print('ALL_OPEN_FLAGS: ', ALL_OPEN_FLAGS)

# yifeilatest1
linux_dir = '/mcfs/Linux_Kernel_Install/linux-6.3'

# Kernel directories to search
linux_dirs = [linux_dir, 
                linux_dir + '/fs/ext4', 
                linux_dir + '/fs/xfs', 
                linux_dir + '/fs/btrfs',
                linux_dir + '/fs']

# csv header 
labels = ['All-Linux-src',
            'Ext4-src',
            'XFS-src',
            'BtrFS-src',
            'All-FS-src']

percent_suffix = '-percent'
percent_labels = [ label + percent_suffix for label in labels ]

# Search for C source files only
pattern = '*.c'

if need_search:
    for i in range(len(linux_dirs)):
        linux_dir = linux_dirs[i]
        open_flag_cnt = {}
        for flag in ALL_OPEN_FLAGS:
            open_flag_cnt[flag] = 0
        for root, dirnames, filenames in os.walk(linux_dir):
            for fn in fnmatch.filter(filenames, pattern):
                abs_fn = os.path.abspath(os.path.join(root, fn))
                with open(abs_fn, 'r') as f:
                    contents = f.read()
                    for flag in ALL_OPEN_FLAGS:
                        count = contents.count(flag)
                        open_flag_cnt[flag] += count
        if print_all:
            print(labels[i] + ': ')
            print(open_flag_cnt)
            print('===============')
        # Save the dict to a pkl file
        with open('{}_open_flag_count.pkl'.format(labels[i]), 'wb') as f:
            pickle.dump(open_flag_cnt, f)

# Read the pkl files and save the results to a csv summary file
all_open_flag_cnt = {}
for i in range(len(labels)):
    with open('{}_open_flag_count.pkl'.format(labels[i]), 'rb') as f:
        open_flag_cnt = pickle.load(f)
        all_open_flag_cnt[labels[i]] = open_flag_cnt        

total_open_flag_cnt = {}
for label in labels:
    total_cnt = 0
    for flag in ALL_OPEN_FLAGS:
        total_cnt += all_open_flag_cnt[label][flag]
    total_open_flag_cnt[label] = total_cnt

header = ['Open_Flag'] + labels + percent_labels

with open('linux_open_flags_summary.csv', 'w') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    for flag in ALL_OPEN_FLAGS:
        data = [flag]
        for i in range(len(labels)):
            data.append(all_open_flag_cnt[labels[i]][flag])
        # Calculate the percentage
        for i in range(len(labels)):
            data.append('{:.2f} %'.format(all_open_flag_cnt[labels[i]][flag] / total_open_flag_cnt[labels[i]] * 100))
        # write the data
        writer.writerow(data) 

print('All completed!')

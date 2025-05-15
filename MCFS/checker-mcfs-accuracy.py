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

from utilities import *

test_type = 'metis'

open_entry = 'syscall_entry_openat:'
open_exit = 'syscall_exit_openat:'

write_entry = 'syscall_entry_write:'
lseek_entry = 'syscall_entry_lseek:'

logname = '/mcfs2/LTTng-xfstests-2022-1211/IOCov/src/mcfs-lttng-mcfs-ext4-256-chdir-fchdir-10m-601.log'

last_line = ''

total_open = 0
total_pair_open = 0

total_write = 0
write_open_pair_case = 0

total_lseek = 0
lseek_open_pair_case = 0

is_mcfs = True
example_write_lines = []

cnt = 0

with open(logname, 'r', encoding="utf8", errors='ignore') as file:
    for line in file:
        cnt += 1
        fg_int = -1
        if open_entry in line:
            fg_list = find_number(line, 'flags = ') 
            if fg_list:
                fg_int = int(fg_list[0])
            fn_list = find_testing_filename(test_type, line, 'filename = ')
            dfd_list = find_number(line, 'dfd = ')
            mcfs_valid_open =  False
            if is_mcfs and fg_int != 0:
                mcfs_valid_open = True
            if fn_list and (not is_mcfs or (is_mcfs and mcfs_valid_open)): 
                last_line = line
                total_open += 1
        #elif open_exit in line:
        #    if open_entry in last_line:
        #        total_pair_open += 1
        #    last_line = ''
        elif write_entry in line:
            total_write += 1
            if open_entry in last_line:
                if len(example_write_lines) < 10:
                    example_write_lines.append(cnt)
                write_open_pair_case += 1
            last_line = ''
        #elif lseek_entry in line:
        #    total_lseek += 1
        #    if open_entry in last_line:
        #        lseek_open_pair_case += 1
        #    last_line = ''        
        else:
            last_line = ''

"""
total_pair_open:  19381011
total_open:  23772932
total_pair_open/total_open:  0.8152553921409441
"""
"""
print('total_pair_open: ', total_pair_open)
print('total_open: ', total_open)
print('total_pair_open/total_open: ', total_pair_open/total_open)

print('total_lseek: ', total_lseek)
print('lseek_open_pair_case: ', lseek_open_pair_case)
"""
print('total_write: ', total_write)
print('write_open_pair_case: ', write_open_pair_case)

print('example_write_lines: ', example_write_lines)

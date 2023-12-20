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

write_entry = 'syscall_entry_write:'
open_exit = 'syscall_exit_openat:'

logname = '/mcfs2/LTTng-xfstests-2022-1211/IOCov/src/mcfs-lttng-mcfs-ext4-256-chdir-fchdir-10m-601.log'

last_line = ''

cnt = 0

last_write_entry = False
fd_write = -1
open_ret = -1

cpu_id_write = -1
cpu_id_open = -1

total_cnt = 0
with open(logname, 'r', encoding="utf8", errors='ignore') as file:
    for line in file:
        if write_entry in line:
            total_cnt += 1
            last_write_entry = True
            fd_list = find_number(line, 'fd = ')
            if fd_list:
                fd_write = int(fd_list[0])
            cpu_id_list = find_cpu_id(line)
            if cpu_id_list:
                cpu_id_write = int(cpu_id_list[0])
        elif open_exit in line and last_write_entry:
            last_write_entry = False
            ret = find_number(line, 'ret = ')
            if ret:
                open_ret = int(ret[0])
            cpu_id_list = find_cpu_id(line)
            if cpu_id_list:
                cpu_id_open = int(cpu_id_list[0])
            if fd_write == open_ret:
                cnt += 1
        else:
            last_write_entry = False
    
print('cnt value: ', cnt)
print('total_cnt value: ', cnt)
print('cnt / total_cnt value: ', cnt / total_cnt)

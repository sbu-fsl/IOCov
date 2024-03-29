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

import sys

logname = '/mcfs2/LTTng-xfstests-2022-1211/IOCov/src/mcfs-lttng-mcfs-ext4-256-chdir-fchdir-10m-601.log'

CPU_num = 4

# entry -> True
# exit -> False
entry_exit = [True] * CPU_num

# current syscall name
sc_names = [''] * CPU_num

# violations
vios = [True] * CPU_num

with open(logname, 'r', encoding="utf8", errors='ignore') as file:
    for line in file:
        if 'entry' in line:
            # get cpu id to check
            

            # 

        elif 'exit' in line:


        else:
            sys.exit('Line is not entry or exit')

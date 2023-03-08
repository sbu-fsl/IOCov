#!/usr/bin/env python3

import sys
from utilities import *

# For each cpu, it is not entry->exit->entry->exit->entry->exit pairs, so has tangling
# possible entry->entry->exit->exit

# Is entry and exit on the same cpu?


logname = '/mcfs2/LTTng-xfstests-2022-1211/IOCov/src/mcfs-lttng-mcfs-ext4-256-chdir-fchdir-10m-601.log'

CPU_num = 4

# entry -> True
# exit -> False
entry_exit = [False] * CPU_num

# current syscall name
sc_names = [''] * CPU_num

# violations
vios = [True] * CPU_num

outliers = 0

with open(logname, 'r', encoding="utf8", errors='ignore') as file:
    for line in file:
        if 'entry' in line:
            # Entry: get cpu id to check
            cpu_id = int(find_cpu_id(line)[0])
            if not entry_exit[cpu_id]:
                entry_exit[cpu_id] = True
            else:
                outliers += 1
                sys.exit('Entry: entry and exit not matching')
            # the system call name
            sc = line.split(' ')[3].split('_')[-1][:-1]
            if sc_names[cpu_id] == '':
                sc_names[cpu_id] = sc
            else:
                outliers += 1
                sys.exit('Entry: system call not matching')
        elif 'exit' in line:
            # Exit: get cpu id to check
            cpu_id = int(find_cpu_id(line)[0])
            if entry_exit[cpu_id]:
                entry_exit[cpu_id] = False
            else:
                outliers += 1
                sys.exit('Exit: entry and exit not matching')
            # the system call name
            sc = line.split(' ')[3].split('_')[-1][:-1]
            if sc_names[cpu_id] == sc:
                sc_names[cpu_id] = ''
            else:
                outliers += 1
                sys.exit('Exit: system call not matching')
        else:
            sys.exit('Line is not entry or exit')

print('All completed')

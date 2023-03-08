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

sc_names = []
# current syscall name
for i in range(CPU_num):
    sc_names.append({})

all_sc_names = {}

with open(logname, 'r', encoding="utf8", errors='ignore') as file:
    for line in file:
        if 'entry' in line:
            # Entry: get cpu id to check
            cpu_id = int(find_cpu_id(line)[0])
            # the system call name
            sc = line.split(' ')[3].split('_')[-1][:-1]
            if sc in sc_names[cpu_id].keys():
                sc_names[cpu_id][sc] += 1
            else:
                sc_names[cpu_id][sc] = 1
            if sc in all_sc_names.keys():
                all_sc_names[sc] += 1
            else:
                all_sc_names[sc] = 1
        elif 'exit' in line:
            # Exit: get cpu id to check
            cpu_id = int(find_cpu_id(line)[0])
            # the system call name
            sc = line.split(' ')[3].split('_')[-1][:-1]
            sc_names[cpu_id][sc] -= 1
            all_sc_names[sc] -= 1
            #if sc_names[cpu_id][sc] < 0:
            #    print(line)
            #    print('Error: no matching entry and exit')            
        else:
            sys.exit('Line is not entry or exit')

print('All completed')
print('sc_names: ', sc_names)
print('all_sc_names: ', all_sc_names)

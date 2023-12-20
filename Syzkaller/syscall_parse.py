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
import re
import sys
# Make sure you are in Syzkaller folder
sys.path.append('../src')
from constants import *

import openpyxl

workbook = openpyxl.Workbook()

# function to get the arguments
def between_brackets(str):
    index1 = str.find('(')
    index2 = str.rfind(')')

    return str[:index1], str[index1+1:index2]

input_dir = '/home/ubuntu/syzkaller/yf-syz-webdump-2023-0706/Syzwebs-40mins-2023-0809-0037/only-inputs'
xlsx_suffix = input_dir.split('/')[-2].split('-', 1)[-1]

# mydict key: every system call name, value: 2d-list
# 2d-list: list of each syscall name and arguments
mydict = {}

# Populate xlsx headers for each syscall
for call in SYZKALLER_SYSCALLS:
    mydict[call] = [SYZKALLER_HEADERS[call]]

# List all the webpage files in the only-inputs directory
for filename in os.listdir(input_dir):
    file = os.path.join(input_dir, filename)
    with open(file) as f:
        lines = f.readlines()

    # For each syscall (belonging to each sheet) in one xlsx file
    for call in SYZKALLER_SYSCALLS:
        for line in lines:
            # Parse Syzkaller syscall sequence
            call_str, rest_str = between_brackets(line)

            # If the call_str matches a call in the "SYZKALLER_SYSCALLS"
            inter_call = [word.strip() for word in call_str.split('=')][-1]
            extracted_call = [word.strip() for word in inter_call.split('$')][0]

            # Caveat: may contain duplicate items for syscall variants (e.g., open, openat)
            # If syscall name matches
            if call == extracted_call:
                # Number of the arguments
                args_num = len(rest_str.split(','))
                # Exceptions --- open: 2 args or 3 args; openat: 3 args or 4 args
                if call in SYZKALLER_ARGS_EXCEPTIONS:
                    if (call == 'open' and (args_num == 2 or args_num == 3)) or (call == 'openat' and (args_num == 3 or args_num == 4)):
                        mydict[call].append([call_str] + rest_str.split(','))
                # Only retain the syscalls with the exact number of arguments
                # +1 due to the "syscall" first header 
                elif args_num + 1 == len(SYZKALLER_HEADERS[call]):
                    # Append syscall name and all the arguments as a sub-list
                    # Ex. append: ['r0 = openat$vcs', '0xffffffffffffff9c', ' &(0x7f0000000000)', ' 0x0', ' 0x0']
                    mydict[call].append([call_str] + rest_str.split(','))
    

for call in SYZKALLER_SYSCALLS:
    new_sheet = workbook.create_sheet(call)
    workbook.active = new_sheet
    sheet = workbook.active
    for row in mydict[call]:
        sheet.append(row)

workbook.save('raw-syzkaller-syscalls-{}.xlsx'.format(xlsx_suffix))

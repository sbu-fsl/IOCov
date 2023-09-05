#!/usr/bin/env python3

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

#input_dir = '/home/ubuntu/syzkaller/yf-syz-webdump-2023-0706/Syzwebs-40mins-2023-0809-0037/only-inputs'
input_dir = '/mnt/c/Users/Rohan/syzkaller/syscall_txt'
xlsx_suffix = input_dir.split('/')[-2].split('-', 1)[-1]

# mydict key: every system call name, value: 2d-list
# 2d-list: list of each syscall name and arguments
mydict = {}

# Populate xlsx headers for each syscall
for call in SYZKALLER_SYSCALLS_NEW:
    mydict[call] = [SYZKALLER_HEADERS[call]]


# List all the webpage files in the only-inputs directory
for filename in os.listdir(input_dir):
    file = os.path.join(input_dir, filename)
    curr_syscall = filename[:filename.find('_')]
    print(curr_syscall)
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            if '(' in line and ')' in line:

                call_str, rest_str = between_brackets(line)
               # print(call_str)
                args_num = len(rest_str.split(','))
                if curr_syscall in SYZKALLER_ARGS_EXCEPTIONS:
                    if (curr_syscall == 'open' and (args_num == 2 or args_num == 3)) or (curr_syscall == 'openat' and (args_num == 3 or args_num == 4)):
                        mydict[curr_syscall].append([call_str] + rest_str.split(','))

                elif args_num + 1 == len(SYZKALLER_HEADERS[curr_syscall]):
                    mydict[curr_syscall].append([call_str] + rest_str.split(','))

#print(mydict[:5])
for call in SYZKALLER_SYSCALLS_NEW:
    new_sheet = workbook.create_sheet(call)
    workbook.active = new_sheet
    sheet = workbook.active
    for row in mydict[call]:
        sheet.append(row)

workbook.save('raw-syzkaller-syscalls-{}.xlsx'.format(xlsx_suffix))                   
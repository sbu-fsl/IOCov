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

directory = '/home/ubuntu/syzkaller/yf-syz-webdump-2023-0706/Syzwebs-18mins-2023-0707-0410/only-inputs'

# mydict key: every system call name, value: 2d-list
# 2d-list: list of each syscall name and arguments
mydict = {}

# Populate header for each syscall
for call in SYZKALLER_SYSCALLS:
    mydict[call] = [SYZKALLER_HEADERS[call]]

# List all the webpage files in the directory
for filename in os.listdir(directory):
    file = os.path.join(directory, filename)
    with open(file) as f:
        lines = f.readlines()

    for call in SYZKALLER_SYSCALLS:
        for line in lines:
            # Parse Syzkaller syscall sequence
            call_str, rest_str = between_brackets(line)

            # If the call_str matches a call in the "SYZKALLER_SYSCALLS"
            inter_call = [word.strip() for word in call_str.split('=')][-1]
            extracted_call = [word.strip() for word in inter_call.split('$')][0]

            # Caveat: may contain duplicate items for syscall variants (e.g., open, openat)
            if call == extracted_call:
                # Append syscall name and all the arguments as a sub-list
                # Ex. append: ['r0 = openat$vcs', '0xffffffffffffff9c', ' &(0x7f0000000000)', ' 0x0', ' 0x0']
                mydict[call].append([call_str] + rest_str.split(','))
    

for call in SYZKALLER_SYSCALLS:
    new_sheet = workbook.create_sheet(call)
    workbook.active = new_sheet
    sheet = workbook.active
    for row in mydict[call]:
        sheet.append(row)

workbook.save('raw-syzkaller-syscalls.xlsx')

import os
import re

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

# We are focusing on SYZKALLER_SYSCALLS related to file systems and supported by IOCov for now
SYZKALLER_SYSCALLS = ['open', 'openat', 'creat', 'openat2', 
            'read', 'pread64', 'write', 'pwrite64',
            'lseek', 'llseek', 'truncate', 'ftruncate', 
            'mkdir', 'mkdirat', 'chmod', 'fchmod', 'fchmodat', 
            'close', 'close_range', 'chdir', 'fchdir', 
            'setxattr', 'lsetxattr', 'fsetxattr', 
            'getxattr', 'lgetxattr', 'fgetxattr']

SYZKALLER_HEADERS = {
    'open': ['syscall', 'pathname', 'flags', 'mode'],
    'openat': ['syscall', 'dirfd', 'pathname', 'flags', 'mode'],
    'creat': ['syscall', 'pathname', 'mode'],
    'openat2': ['syscall', 'dirfd', 'pathname', 'how', 'size'],
    'read': ['syscall', 'fd', 'buf', 'count'],
    'pread64': ['syscall', 'fd', 'buf', 'count', 'offset'],
    'write': ['syscall', 'fd', 'buf', 'count'],
    'pwrite64': ['syscall', 'fd', 'buf', 'count', 'offset'],
    'lseek': ['syscall', 'fd', 'offset', 'whence'],
    'llseek': ['syscall', 'fd', 'offset_high', 'offset_low', 'result', 'whence'],
    'truncate': ['syscall', 'path', 'length'],
    'ftruncate': ['syscall', 'fd', 'length'],
    'mkdir': ['syscall', 'pathname', 'mode'],
    'mkdirat': ['syscall', 'dirfd', 'pathname', 'mode'],
    'chmod': ['syscall', 'pathname', 'mode'],
    'fchmod': ['syscall', 'fd', 'mode'],
    'fchmodat': ['syscall', 'dirfd', 'pathname', 'mode', 'flags'],
    'close': ['syscall', 'fd'],
    'close_range': ['syscall', 'first', 'last', 'flags'],
    'chdir': ['syscall', 'path'],
    'fchdir': ['syscall', 'fd'],
    'setxattr': ['syscall', 'path', 'name', 'value', 'size', 'flags'],
    'lsetxattr': ['syscall', 'path', 'name', 'value', 'size', 'flags'],
    'fsetxattr': ['syscall', 'fd', 'name', 'value', 'size', 'flags'],
    'getxattr': ['syscall', 'path', 'name', 'value', 'size'],
    'lgetxattr': ['syscall', 'path', 'name', 'value', 'size'],
    'fgetxattr': ['syscall', 'fd', 'name', 'value', 'size']
}

# Populate header for each syscall
for call in SYZKALLER_SYSCALLS:
    mydict[call] = [[]]

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
            # Caveat: may contain duplicate items for syscall variants (e.g., open, openat)
            if call in call_str:
                # Append syscall name and all the arguments as a sub-list
                # Ex. append: ['r0 = openat$vcs', '0xffffffffffffff9c', ' &(0x7f0000000000)', ' 0x0', ' 0x0']
                mydict[call].append([call_str] + rest_str.split(','))
    

for call in SYZKALLER_SYSCALLS:
    new_sheet = workbook.create_sheet(call)
    workbook.active = new_sheet
    sheet = workbook.active
    for row in mydict[call]:
        sheet.append(row)

workbook.save('SYZKALLER_SYSCALLS.xlsx')

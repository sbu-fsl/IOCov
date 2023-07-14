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

mydict = {}

# We are focusing on syscalls related to file systems and supported by IOCov for now
syscalls = ['open', 'openat', 'creat', 'openat2', 
            'read', 'pread64', 'write', 'pwrite64',
            'lseek', 'llseek', 'truncate', 'ftruncate', 
            'mkdir', 'mkdirat', 'chmod', 'fchmod', 'fchmodat', 
            'close', 'close_range', 'chdir', 'fchdir', 
            'setxattr', 'lsetxattr', 'fsetxattr', 
            'getxattr', 'lgetxattr', 'fgetxattr']

for call in syscalls:
    mydict[call] = [[]]

# List all the webpage files in the directory
for filename in os.listdir(directory):
    file = os.path.join(directory, filename)
    with open(file) as f:
        lines = f.readlines()

    for call in syscalls:
        for line in lines:
            # Parse Syzkaller syscall sequence
            call_str, rest_str = between_brackets(line)

            # If the call_str matches a call in the 'syscalls'
            if call in call_str:
                # Append syscall name and all the arguments as a sub-list
                mydict[call].append([call_str] + rest_str.split(','))
    

for call in syscalls:
    new_sheet = workbook.create_sheet(call)
    workbook.active = new_sheet
    sheet = workbook.active
    for row in mydict[call]:
        sheet.append(row)

workbook.save('syscalls.xlsx')

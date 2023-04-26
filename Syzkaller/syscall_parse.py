import os
import re

import openpyxl

workbook = openpyxl.Workbook()

# function to get the arguments
def between_brackets(str):
    index1 = str.find("(")
    index2 = str.rfind(")")

    return str[:index1], str[index1+1:index2]
directory = '/mnt/c/Users/Rohan/html'

mydict = {}

# We are focusing on syscalls related to file systems for now
syscalls = ["open","openat","creat","openat2","read","pread64","write","pwrite64","lseek","llseek","truncate","ftruncate","mkdir","mkdirat","chmod","fchmod","fchmodat","close","close_range","chdir","fchdir","setxattr","lsetxattr","fsetxattr","getxattr","lgetxattr","fgetxattr","read"]

for call in syscalls:
    mydict[call] = [[]]


for filename in os.listdir(directory):
    file = os.path.join(directory, filename)
    with open(file) as f:
        lines = f.readlines()

    for call in syscalls:
        for line in lines:
            call_str, rest_str = between_brackets(line)

            if call in call_str:
                mydict[call].append([call_str] + rest_str.split(','))
    

for call in syscalls:
    new_sheet = workbook.create_sheet(call)
    workbook.active = new_sheet
    sheet = workbook.active
    for row in mydict[call]:
        sheet.append(row)

workbook.save('syscalls.xlsx')

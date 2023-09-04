import os
import re

import openpyxl

SYSCALLS = ["open", "read", "write", "lseek", "close", 
            "truncate", "unlink", "mkdir", "rmdir", "chmod", 
            "chown", "setxattr", "removexattr", "getxattr", "rename", "link", "symlink", "statfs"]
#SYSCALLS = ["mkdir"]


for syscall in SYSCALLS:
    syscall_file = syscall + "_debug.txt"
    syscall_file_f = open(syscall_file, "a")
    f = open("debug_out.log", "rb")
    for x in f:
        text = x.decode('utf8', errors='ignore')
        if " "+ syscall+"(" in text and text[0]=='#':
            syscall_file_f.write(text)
            #print("here")
    print(syscall)
    syscall_file_f.close()
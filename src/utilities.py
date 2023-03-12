#!/usr/bin/env python3

from constants import *
import re

###### Parser Utilities
# Apply to any postive/negative numbers
def find_number(text, c):
    return re.findall(r'%s([-]?\d+)' % c, text)

def find_cpu_id(text):
    return find_number(text, 'cpu_id = ')

### RegEx matching for pathname
## xfstests
def find_xfstests_filename(text, c):
    return re.findall(r'%s(\"/mnt.*\")' % c, text)

# MCFS: everything inside MCFS test mountpoint
def find_mcfs_name(text, c):
    return re.findall(r'%s(\"/mnt/test-ext4-i0-s0.*\")' % c, text)

# MCFS: all the files inside MCFS test mountpoint
def find_mcfs_filename(text, c):
    return re.findall(r'%s(\"/mnt/test-ext4-i0-s0/.*f-0[0-9]\")' % c, text)

# CrashMonkey: everything inside /mnt/snapshot
def find_crashmonkey_filename(text, c):
    return re.findall(r'%s(\"/mnt/snapshot.*\")' % c, text)

def find_testing_filename(text, c):
    return find_mcfs_filename(text, c)

# Does not collect input coverage for close()
def init_input_cov():
    input_cov = {}
    for sc in ALL_SYSCALLS:
        empty_arg = {}
        if sc == 'open':
            for each_arg in SYSCALL_ARGS[sc]:
                if each_arg == 'flags': # open: flags
                    flag_dict = {}
                    for flag in ALL_OPEN_FLAGS:
                        flag_dict[flag] = 0
                    empty_arg[each_arg] = flag_dict
                else:
                    empty_arg[each_arg] = {} # open: mode
        elif sc == 'lseek':
            for each_arg in SYSCALL_ARGS[sc]:
                if each_arg == 'whence': # lseek: whence
                    whence_dict = {}
                    for whence in ALL_LSEEK_WHENCES:
                        whence_dict[whence] = 0
                    empty_arg[each_arg] = whence_dict
                else:
                    empty_arg[each_arg] = {} # lseek: offset
        elif sc == 'setxattr':
            for each_arg in SYSCALL_ARGS[sc]:
                if each_arg == 'flags': # setxattr: flags
                    flags_dict = {}
                    for flags in ALL_SETXATTR_FLAGS:
                        flags_dict[flags] = 0
                    empty_arg[each_arg] = flags_dict
                else:
                    empty_arg[each_arg] = {} # setxattr: size
        else:
            for each_arg in SYSCALL_ARGS[sc]:
                empty_arg[each_arg] = {}
        input_cov[sc] = empty_arg
    return input_cov

def init_output_cov():
    output_cov = {}
    for sc in ALL_SYSCALLS:
        output_cov[sc] = {}
    return output_cov

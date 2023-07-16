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

# Use find_mcfs_filename for MCFS
# Use find_xfstests_filename for xfstests
def find_testing_filename(text, c):
    return find_xfstests_filename(text, c)

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

# Transform a list of decimal open flags to a dict with individual flags
def interpret_open_flags(open_flags_dec):
    flag_dict = {}
    for flag in ALL_OPEN_FLAGS:
        flag_dict[flag] = 0  
    for flag_dec in open_flags_dec:
        if flag_dec & 1 == 0:
            flag_dict['O_RDONLY'] += 1
        for each_bit in OPEN_BIT_FLAGS:
            if flag_dec & each_bit == each_bit:
                flag_dict[OPEN_BIT_FLAGS[each_bit]] += 1         
    return flag_dict


# Given a list of elements, convert it to a dict
# Key: each unique element (convert num/int to str)
# Value: the frequency of each element
# E.g., for open mode
def list_to_count_dict(input_list):
    input_dict = {}
    for elem in input_list:
        if elem in input_dict.keys():
            input_dict[elem] += 1
        else:
            input_dict[elem] = 1
    return input_dict
    
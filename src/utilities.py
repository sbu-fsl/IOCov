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

"""
Various utilities for IOCov parsing and plotting
"""

from constants import *
import re
import os
import pickle

###### Parser Utilities
# Apply to any postive/negative numbers
def find_number(text, c):
    return re.findall(r'%s([-]?\d+)' % c, text)

def find_cpu_id(text):
    return find_number(text, 'cpu_id = ')

### RegEx matching for pathname
## xfstests
# def find_xfstests_filename(text, c):
#     return re.findall(r'%s\("/mnt/(test|scratch)[^"]*"\)' % c, text)
def find_xfstests_filename(text, c):
    return re.findall(r'%s(\"/mnt.*\")' % c, text)

# MCFS: everything inside MCFS test mountpoint
# def find_mcfs_name(text, c):
#     return re.findall(r'%s\("/mnt/test-[^-]+-i[0-9]-s[0-9][^"]*"\)' % c, text)
def find_mcfs_name(text, c):
    return re.findall(r'%s(\"/mnt/test-ext4-i0-s0.*\")' % c, text)

# MCFS: all the files inside MCFS test mountpoint
# def find_mcfs_filename(text, c):
#     return re.findall(r'%s\("/mnt/test-[^-]+-i[0-9]-s[0-9]/.*f-0[0-9]"\)' % c, text)
def find_mcfs_filename(text, c):
    return re.findall(r'%s(\"/mnt/test-ext4-i0-s0/.*f-0[0-9]\")' % c, text)

# CrashMonkey: everything inside /mnt/snapshot
# def find_crashmonkey_filename(text, c):
#     return re.findall(r'%s\("/mnt/snapshot.*"\)' % c, text)
def find_crashmonkey_filename(text, c):
    return re.findall(r'%s(\"/mnt/snapshot.*\")' % c, text)

# Use find_mcfs_filename or find_mcfs_name for MCFS
# Use find_xfstests_filename for xfstests
# Use find_crashmonkey_filename for CrashMonkey
def find_testing_filename(test_type, text, c):
    if test_type == 'xfstests':
        return find_xfstests_filename(text, c)
    elif test_type == 'metis':
        return find_mcfs_filename(text, c)
    elif test_type == 'crashmonkey':
        return find_crashmonkey_filename(text, c)
    else:
        raise ValueError('Invalid test type: {}'.format(test_type))

# Does not collect input coverage for close()
def init_input_cov():
    input_cov = {}
    for sc in ALL_SYSCALLS_NEW:
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

def list_to_whence_dict(whence_list):
    whence_dict = {}
    for whence in ALL_LSEEK_WHENCES:
        whence_dict[whence] = 0
    for whence_dec in whence_list:
        if whence_dec < len(ALL_LSEEK_WHENCES):
            whence_dict[LSEEK_WHENCE_NUMS[whence_dec]] += 1
    return whence_dict

def list_to_setxattr_flags_dict(flags_list):
    flags_dict = {}
    for flags in ALL_SETXATTR_FLAGS:
        flags_dict[flags] = 0
    for flags_dec in flags_list:
        if flags_dec < len(ALL_SETXATTR_FLAGS):
            flags_dict[SETXATTR_FLAGS_NUMS[flags_dec]] += 1
    return flags_dict


def read_write_count_by_pkl(pkl_dir, pkl_file):
    fig5_xfstests_input_coords = {}

    with open(os.path.join(pkl_dir, pkl_file), 'rb') as f:
        fig5_xfstests_input_coords = pickle.load(f)

    xfstests_write_count = fig5_xfstests_input_coords['write']['count']

    X_xfstests = xfstests_write_count['X-axis']
    Y_xfstests = xfstests_write_count['Y-axis']

    # print('xfstests_write_count: ', xfstests_write_count)
    """
    print('len(X_xfstests): ', len(X_xfstests))
    for i in range(len(X_xfstests) - 1, -1, -1):
        if Y_xfstests[i] > 0:
            print('i: ', i)
            print('X_xfstests: ', X_xfstests[i])
            break
    """
    Keep = -1
    for i in range(len(X_xfstests)):
        each_X = X_xfstests[i]
        if each_X == '2^32':
            Keep = i 

    # Labels
    X_cut_xfstests = X_xfstests[0:Keep+1]
    # Real Values
    Y_cut_xfstests = Y_xfstests[0:Keep+1]

    # print('X_cut_xfstests: ', X_cut_xfstests)
    # print('Y_cut_xfstests: ', Y_cut_xfstests)

    # ROUND DOWN: 2^{10} == 1024 (1024 - 2047)
    X_xfstests = []
    Y_xfstests = []
    
    for i in range(len(X_cut_xfstests)):
        if X_cut_xfstests[i] == 'Intv.':
            Y_xfstests[-1] += Y_cut_xfstests[i]
        else: # Not 'Intv.'
            X_xfstests.append(X_cut_xfstests[i])
            Y_xfstests.append(Y_cut_xfstests[i])

    """
    # ONLY BOUNDARY VALUES EXACTLY EQUAL TO POWERS OF 2 NUMBERS
    X_xfstests = []
    Y_xfstests = []
    for i in range(len(X_cut_xfstests)):
        if X_cut_xfstests[i] != 'Intv.':
            X_xfstests.append(X_cut_xfstests[i])
            Y_xfstests.append(Y_cut_xfstests[i])

    X_xfstests.pop(0)
    Y_xfstests.pop(0)
    # print('X_xfstests: ', X_xfstests)
    # print('Y_xfstests: ', Y_xfstests)
    """
    # Do not use 2^10, use 10 instead 
    for i in range(len(X_xfstests)):
        X_xfstests[i] = X_xfstests[i].split('^')[-1]
    
    X_xfstests[0] = 'Equal to 0'
    return X_xfstests, Y_xfstests

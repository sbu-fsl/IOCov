#!/usr/bin/env python3

import pickle
import json
import numpy as np
import os 

pkl_dir = os.getcwd()

# O_RDONLY
# #define O_RDONLY	00000000

# Key: number of flags; Value: percentage
crashmonkey_all_res = {}
xfstests_all_res = {}

crashmonkey_rdonly_res = {}
xfstests_rdonly_res = {}

crashmonkey_open_flags = {}
xfstests_open_flags = {}

with open(os.path.join(pkl_dir, 'open_flag_filtered_crashmonkey.pkl'), 'rb') as f:
    crashmonkey_open_flags = pickle.load(f)

with open(os.path.join(pkl_dir, 'open_flag_filtered_xfstests_xattr_open_dump.pkl'), 'rb') as f:
    xfstests_open_flags = pickle.load(f)

# print('crashmonkey_open_flags: ', crashmonkey_open_flags)

# CrashMonkey
for flag, cnt in crashmonkey_open_flags.items():
    flag_num = bin(flag).count("1")
    # #define O_RDONLY	00000000
    if flag & 1 == 0:
        flag_num += 1
    if flag_num in crashmonkey_all_res.keys():
        crashmonkey_all_res[flag_num] += cnt
    else:
        crashmonkey_all_res[flag_num] = cnt     
    # if O_RDONLY is enabled
    if flag & 1 == 0:
        if flag_num in crashmonkey_rdonly_res.keys():
            crashmonkey_rdonly_res[flag_num] += cnt
        else:
            crashmonkey_rdonly_res[flag_num] = cnt

for flag, cnt in xfstests_open_flags.items():
    flag_num = bin(flag).count("1")
    # #define O_RDONLY	00000000
    if flag & 1 == 0:
        flag_num += 1
    if flag_num in xfstests_all_res.keys():
        xfstests_all_res[flag_num] += cnt
    else:
        xfstests_all_res[flag_num] = cnt     
    # if O_RDONLY is enabled
    if flag & 1 == 0:
        if flag_num in xfstests_rdonly_res.keys():
            xfstests_rdonly_res[flag_num] += cnt
        else:
            xfstests_rdonly_res[flag_num] = cnt

def transform_to_percentage(res):
    sum_val = sum(res.values())
    for key in res:
        res[key] = round(res[key] / sum_val * 100, 2)
    
    res = {k: res[k] for k in sorted(res)}
    return res

crashmonkey_all_res = transform_to_percentage(crashmonkey_all_res)
xfstests_all_res = transform_to_percentage(xfstests_all_res)

crashmonkey_rdonly_res = transform_to_percentage(crashmonkey_rdonly_res)
xfstests_rdonly_res = transform_to_percentage(xfstests_rdonly_res)

print('crashmonkey_all_res: ', crashmonkey_all_res)
print('xfstests_all_res: ', xfstests_all_res)

print('crashmonkey_rdonly_res: ', crashmonkey_rdonly_res)
print('xfstests_rdonly_res: ', xfstests_rdonly_res)

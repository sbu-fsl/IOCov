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

from constants import *
import pickle
import sys

# Input coverage
def get_syscall_count_from_pkl(pkl_path):
    input_cov = {}
    input_count = {}
    with open(pkl_path, 'rb') as f:
        input_cov = pickle.load(f)
    if not input_cov:
        sys.exit('Cannot load pkl file for analysis')
    for sc in SC_COUNT_ARGS.keys():
        input_count[sc] = 0

    for sc, arg in SC_COUNT_ARGS.items():
        input_vals = input_cov[sc][arg]
        for val in input_vals.values():
            input_count[sc] += val 
    return input_count

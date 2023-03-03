#!/usr/bin/env python3

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

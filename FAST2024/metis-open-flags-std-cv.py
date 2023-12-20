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

import statistics
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import numpy as np
import os
import pickle
from scipy.stats import gmean
import math

pkl_dir = '/mcfs/iocov-mcfs-fast24-2023-0723/IOCov/FAST2024/input-pickles'

pkl_files = ['input-cov-mcfs-Uniform-50p-40mins-open-flags-20230905-003428-1106728.pkl']

labels = ['Metis-open-flags-Uniform-50p-40mins']
x_labels = []

all_open_flags = []

num_tools = len(pkl_files)
for i in range(num_tools):
    with open(os.path.join(pkl_dir, pkl_files[i]), 'rb') as f:
        input_data = pickle.load(f)
        all_open_flags.append(input_data['open']['flags'])

ignored_flags = ['O_ACCMODE', 'O_RDONLY']

# Init a list which includes num_tools sub lists [ []*num_tools ]
# Have to use this way to create empty sublists
all_data = [[] for _ in range(num_tools)]

# For each specific open flag
for open_flag in sorted(all_open_flags[0].keys()):
    if open_flag not in ignored_flags:
        x_labels.append(open_flag)
        for i in range(num_tools):
            all_data[i].append(all_open_flags[i][open_flag])

all_data_arr = np.array(all_data)

print('all_data_arr: ', all_data_arr)

# Compute means of each subarray
means = np.mean(all_data_arr, axis=1)

# Compute standard deviations of each subarray
std_devs = np.std(all_data_arr, axis=1)

# Compute CVs
print('std_devs: ', std_devs)
print('means: ', means)

cvs = (std_devs / means) * 100

print('coefficient of variation (CV): ', cvs)

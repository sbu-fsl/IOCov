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

import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import sys
sys.path.append('../src')
from utilities import *

pkl_dir = '/mcfs/iocov-mcfs-fast24-2023-0723/IOCov/FAST2024/input-pickles'

coord_pkl_files = ['mcfs-Uniform-40mins-33parts-write-sizes-20230913-024218-2957359_input_coords.pkl',
                   'mcfs-Uniform-4hours-write-sizes-20230907-001716-1330916_input_coords.pkl', 
                   'mcfs-Uniform-24hours-33parts-write-sizes-20230908-024720-1683195_input_coords.pkl' 
                   ]

labels = ['Metis-write-size-Uniform-40mins', 'Metis-write-size-Uniform-4hours', 'Metis-write-size-Uniform-24hours']

num_tools = len(coord_pkl_files)

# Key: testing tool (in labels)
# Value: list of X and Y coordinates for the corresponding testing tool
all_axes = {}

for i in range(len(coord_pkl_files)):
    X_tests, Y_tests = read_write_count_by_pkl(pkl_dir, coord_pkl_files[i])
    all_axes[labels[i]] = [X_tests, Y_tests]

x_labels = all_axes[labels[0]][0]

Y_data = []

for i in range(len(labels)):
    Y_data.append(all_axes[labels[i]][1])

Y_data = np.array(Y_data)

print('Y_data.shape:', Y_data.shape)
print('Y_data:', Y_data)

std_deviations = [np.std(sublist[:-1]) for sublist in Y_data]
print('std_deviations: ', std_deviations)
print('type(std_deviations): ', type(std_deviations))

# Sum of each sublist
means = [np.mean(sublist[:-1]) for sublist in Y_data]
print('means: ', means)
print('type(means): ', type(means))

# Compute Coefficient of Variations (CVs)
cvs = [(std_dev / mean) * 100 for mean, std_dev in zip(means, std_deviations)]

# Print the results
for i, std in enumerate(std_deviations):
    print(f"Standard Deviation of Sublist {i + 1}: {std}")

for i, cv in enumerate(cvs):
    print(f"Coefficient of Variation (CV) of Sublist {i + 1}: {cv}")


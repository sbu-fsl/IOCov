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
import os
import pickle

plt.rcParams["font.family"] = "Times New Roman"

pkl_dir = '/mcfs2/LTTng-xfstests-2022-1211/IOCov/src'

fig3_iocov_mcfs_precision = {}
fig3_mcfs_filter_ratio = {}
dpi_val = 600

with open(os.path.join(pkl_dir, 'fig3_iocov_mcfs_precision.pkl'), 'rb') as f:
    fig3_iocov_mcfs_precision = pickle.load(f)

with open(os.path.join(pkl_dir, 'fig3_mcfs_filter_ratio.pkl'), 'rb') as f:
    fig3_mcfs_filter_ratio = pickle.load(f)

# print('fig3_iocov_mcfs_precision: ', fig3_iocov_mcfs_precision)
# print('fig3_mcfs_filter_ratio: ', fig3_mcfs_filter_ratio)

data1_precision = []
data2_filter_ratio = []

x_labels = []

for sc in fig3_iocov_mcfs_precision.keys():
    x_labels.append(sc)
    data1_precision.append(fig3_iocov_mcfs_precision[sc])
    data2_filter_ratio.append(fig3_mcfs_filter_ratio[sc])

# print('x_labels: ', x_labels)
# print('data1_precision: ', data1_precision)
# print('data2_filter_ratio: ', data2_filter_ratio)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

ax1.bar(x_labels, data1_precision)
ax2.bar(x_labels, data2_filter_ratio)

fig.subplots_adjust(wspace=0.3)
# ax1.set_title('Precision')
ax1.yaxis.grid(True)
ax1.set_xlabel('System Calls')
ax1.set_ylabel('Filter Precision (%)')

# ax2.set_title('Filter Ratio')
ax2.set_yscale('log')
ax2.yaxis.grid(True)

ax2.set_xlabel('System Calls')
ax2.set_ylabel('Filter Ratio (log scale)')

plt.savefig('mcfs-precision-filter-ratio.pdf', format = 'pdf', bbox_inches='tight', dpi=dpi_val)

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
import math
import matplotlib as mpl
import matplotlib.ticker as ticker

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# Set the font size globally
mpl.rcParams['font.size'] = 10

plt.rcParams["font.family"] = "Times New Roman"

# pkl_dir = '/mcfs2/LTTng-xfstests-2022-1211/IOCov/src'
pkl_dir = os.getcwd()

fig7_xfstests_input = {}
fig7_crashmonkey_input = {}
fig7_syzkaller_input = {}
fig7_metis_uniform_input = {}
fig7_metis_rsd_input = {}
fig7_metis_irsd_input = {}

dpi_val = 600

with open(os.path.join(pkl_dir, 'fig4_input_cov_all_xfstests_xattrs.pkl'), 'rb') as f:
    fig7_xfstests_input = pickle.load(f)

with open(os.path.join(pkl_dir, 'fig4_input_cov_crashmonkey.pkl'), 'rb') as f:
    fig7_crashmonkey_input = pickle.load(f)

with open(os.path.join(pkl_dir, 'input-cov-syzkaller-debug-40mins-2023-0830.pkl'), 'rb') as f:
    fig7_syzkaller_input = pickle.load(f)

with open(os.path.join(pkl_dir, 'input-cov-mcfs-Uniform-50p-40mins-open-flags-20230905-003428-1106728.pkl'), 'rb') as f:
    fig7_metis_uniform_input = pickle.load(f)

with open(os.path.join(pkl_dir, 'input_cov_mcfs_Prob_5factor_40mins_open_flags_20230810_181953_484817.pkl'), 'rb') as f:
    fig7_metis_rsd_input = pickle.load(f)

with open(os.path.join(pkl_dir, 'input-cov-mcfs-WHM-inverse-40mins-open-flags-20230817-024926-918867.pkl'), 'rb') as f:
    fig7_metis_irsd_input = pickle.load(f)


fig7_xfstests_open_flags = fig7_xfstests_input['open']['flags']
fig7_crashmonkey_open_flags = fig7_crashmonkey_input['open']['flags']
fig7_syzkaller_open_flags = fig7_syzkaller_input['open']['flags']
fig7_metis_uniform_open_flags = fig7_metis_uniform_input['open']['flags']
fig7_metis_rsd_open_flags = fig7_metis_rsd_input['open']['flags']
fig7_metis_irsd_open_flags = fig7_metis_irsd_input['open']['flags']

# print('fig7_xfstests_open_flags: ', fig7_xfstests_open_flags)
# print('fig7_crashmonkey_open_flags: ', fig7_crashmonkey_open_flags)

def log2_with_zero(values):
    log2_values = []
    for value in values:
        if value == 0:
            log2_values.append(0)  # Set log2(0) to 0
        else:
            log2_values.append(math.log2(value))
    return log2_values

flag_list = []
xfstests_list = []
crashmonkey_list = []
syzkaller_list = []
metis_uniform_list = []
metis_rsd_list = []
metis_irsd_list = []

for open_flag in fig7_xfstests_open_flags.keys():
    flag_list.append(open_flag)
    xfstests_list.append(fig7_xfstests_open_flags[open_flag])
    crashmonkey_list.append(fig7_crashmonkey_open_flags[open_flag])
    syzkaller_list.append(fig7_syzkaller_open_flags[open_flag])
    metis_uniform_list.append(fig7_metis_uniform_open_flags[open_flag])
    metis_rsd_list.append(fig7_metis_rsd_open_flags[open_flag])
    metis_irsd_list.append(fig7_metis_irsd_open_flags[open_flag])

xfstests_log = log2_with_zero(xfstests_list)
crashmonkey_log = log2_with_zero(crashmonkey_list)
syzkaller_log = log2_with_zero(syzkaller_list)
metis_uniform_log = log2_with_zero(metis_uniform_list)
metis_rsd_log = log2_with_zero(metis_rsd_list)
metis_irsd_log = log2_with_zero(metis_irsd_list)

# X axis
targets = [10, 100, 1000, 10000, 100000, 1000000, 10000000]

targets_log = log2_with_zero(targets)

# print('xfstests_log: ', xfstests_log)
# print('crashmonkey_log: ', crashmonkey_log)
# print('targets_log: ', targets_log)

def rmsd(coords1, coords2):
    # Align the two sets of coordinates
    # ...

    # Calculate the distance between corresponding atoms
    distances = []
    for i in range(len(coords1)):
        diff = coords1[i] - coords2[i]
        distance = np.sqrt(np.sum(diff**2))
        distances.append(distance)

    # Square the distances and take the mean
    mean_squared_distance = np.mean(np.array(distances)**2)

    # Take the square root of the mean squared distance
    rmsd = np.sqrt(mean_squared_distance)

    return rmsd

labels = ['CrashMonkey', 'xfstests', 'syzkaller', 'metis-uniform', 'metis-rsd', 'metis-irsd']
# Y axis
xfstests_rmsd_res = []
crashmonkey_rmsd_res = []
syzkaller_rmsd_res = []
metis_uniform_rmsd_res = []
metis_rsd_rmsd_res = []
metis_irsd_rmsd_res = []

flag_cnt = len(xfstests_log)

for i in range(len(targets_log)):
    target_val = targets_log[i]
    target_temp = [target_val] * flag_cnt
    xfstests_rmsd = rmsd(xfstests_log, target_temp)
    crashmonkey_rmsd = rmsd(crashmonkey_log, target_temp)
    syzkaller_rmsd = rmsd(syzkaller_log, target_temp)
    metis_uniform_rmsd = rmsd(metis_uniform_log, target_temp)
    metis_rsd_rmsd = rmsd(metis_rsd_log, target_temp)
    metis_irsd_rmsd = rmsd(metis_irsd_log, target_temp)
    # append the RMSD values
    xfstests_rmsd_res.append(xfstests_rmsd)
    crashmonkey_rmsd_res.append(crashmonkey_rmsd)
    syzkaller_rmsd_res.append(syzkaller_rmsd)
    metis_uniform_rmsd_res.append(metis_uniform_rmsd)
    metis_rsd_rmsd_res.append(metis_rsd_rmsd)
    metis_irsd_rmsd_res.append(metis_irsd_rmsd)

# print('xfstests_rmsd_res: ', xfstests_rmsd_res)
# print('crashmonkey_rmsd_res: ', crashmonkey_rmsd_res)

xtick_values = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
# xtick_labels = ['0', '1', '2', '3 (1K)', '4', '5', '6 (1M)', '7 (10M)']
xtick_labels = ['0', '10', '100', '1K', '10K', '100K', '1M', '10M']

# fig, ax = plt.subplots(figsize=(3.2, 1.6))
# Larger figure
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(targets, crashmonkey_rmsd_res, linewidth=2, color='blue', linestyle='-', marker='o', label='CrashMonkey')
ax.plot(targets, xfstests_rmsd_res, linewidth=2, color='red', linestyle='--', marker='s', label='xfstests')
ax.plot(targets, syzkaller_rmsd_res, linewidth=2, color='green', linestyle=':', marker='^', label='Syzkaller')
ax.plot(targets, metis_uniform_rmsd_res, linewidth=2, color='purple', linestyle='-.', marker='+', label='Metis Uniform')
ax.plot(targets, metis_rsd_rmsd_res, linewidth=2, color='orange', linestyle='-', marker='*', label='Metis RSD')
ax.plot(targets, metis_irsd_rmsd_res, linewidth=2, color='black', linestyle='--', marker='D', label='Metis IRSD')

ax.set_xscale('log')

plt.xticks(xtick_values, xtick_labels)
# ax.set_xlim(xmin = 0.1)
ax.set_ylim(bottom=0)
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))

ax.legend(loc='best', fontsize=10)

# Add a title and axis labels
# plt.title('Line Plot Example')
ax.set_xlabel('Target Value (log scale base 10)', fontweight='bold')
ax.set_ylabel('TCD Value', fontweight='bold')

ax.set_axisbelow(True)
ax.grid(axis='y', linestyle='-', alpha=0.3)

# Adjust the plot layout
plt.tight_layout()

# Save the plot as a PDF file
# plt.savefig('tcd-rmsd-open-flags-extended.pdf', format='pdf', bbox_inches='tight')
plt.savefig('tcd-rmsd-open-flags-extended.png', format='png', dpi=600, bbox_inches='tight')

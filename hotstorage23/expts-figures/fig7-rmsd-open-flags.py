#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import math

plt.rcParams["font.family"] = "Times New Roman"

# pkl_dir = '/mcfs2/LTTng-xfstests-2022-1211/IOCov/src'
pkl_dir = os.getcwd()

fig7_xfstests_input = {}
fig7_crashmonkey_input = {}
dpi_val = 600

with open(os.path.join(pkl_dir, 'fig4_input_cov_all_xfstests_xattrs.pkl'), 'rb') as f:
    fig7_xfstests_input = pickle.load(f)

with open(os.path.join(pkl_dir, 'fig4_input_cov_crashmonkey.pkl'), 'rb') as f:
    fig7_crashmonkey_input = pickle.load(f)


fig7_xfstests_open_flags = fig7_xfstests_input['open']['flags']
fig7_crashmonkey_open_flags = fig7_crashmonkey_input['open']['flags']

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
for open_flag in fig7_xfstests_open_flags.keys():
    flag_list.append(open_flag)
    xfstests_list.append(fig7_xfstests_open_flags[open_flag])
    crashmonkey_list.append(fig7_crashmonkey_open_flags[open_flag])

xfstests_log = log2_with_zero(xfstests_list)
crashmonkey_log = log2_with_zero(crashmonkey_list)

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

# Y axis
xfstests_rmsd_res = []
crashmonkey_rmsd_res = []

flag_cnt = len(xfstests_log)

for i in range(len(targets_log)):
    target_val = targets_log[i]
    target_temp = [target_val] * flag_cnt
    xfstests_rmsd = rmsd(xfstests_log, target_temp)
    crashmonkey_rmsd = rmsd(crashmonkey_log, target_temp)
    xfstests_rmsd_res.append(xfstests_rmsd)
    crashmonkey_rmsd_res.append(crashmonkey_rmsd)

# print('xfstests_rmsd_res: ', xfstests_rmsd_res)
# print('crashmonkey_rmsd_res: ', crashmonkey_rmsd_res)

xtick_values = [10, 100, 1000, 10000, 100000, 1000000, 10000000]
# xtick_labels = ['0', '1', '2', '3 (1K)', '4', '5', '6 (1M)', '7 (10M)']
xtick_labels = ['10', '100', '1K', '10K', '100K', '1M', '10M']

plt.plot(targets, crashmonkey_rmsd_res, color='#4daf4a', linestyle='-', marker='.', label='CrashMonkey')
plt.plot(targets, xfstests_rmsd_res, color='#ff7f0e', linestyle='--', marker='.', label='xfstests')

plt.xscale('log')

plt.xticks(xtick_values, xtick_labels)

plt.legend(loc='best')

# Add a title and axis labels
# plt.title('Line Plot Example')
plt.xlabel('Target Value T (log scale base 10)')
plt.ylabel('RMSD Value')

# Save the plot as a PDF file
plt.savefig('fig7-open-flags-RMSD.pdf', format='pdf', bbox_inches='tight', pad_inches=0.1)

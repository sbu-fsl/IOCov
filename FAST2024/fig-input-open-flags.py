#!/usr/bin/env python3

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

plt.rcParams["font.family"] = "Times New Roman"
dpi_val = 600

pkl_dir = '/mcfs/iocov-mcfs-fast24-2023-0723/IOCov/FAST2024/input-pickles'

xfstests_input = {}
crashmonkey_input = {}
syzkaller_input = {}
# Uniform or prob open inputs
mcfs_uniform_input = {}
mcfs_prob_input = {}
mcfs_prob_inverse_input = {}

with open(os.path.join(pkl_dir, 'fig4_input_cov_all_xfstests_xattrs.pkl'), 'rb') as f:
    xfstests_input = pickle.load(f)

with open(os.path.join(pkl_dir, 'fig4_input_cov_crashmonkey.pkl'), 'rb') as f:
    crashmonkey_input = pickle.load(f)

with open(os.path.join(pkl_dir, 'input_cov_syzkaller_40mins_2023_0809_0037.pkl'), 'rb') as f:
    syzkaller_input = pickle.load(f)

with open(os.path.join(pkl_dir, 'input_cov_mcfs_Uniform_50p_40mins_open_flags_20230810_170456_382883.pkl'), 'rb') as f:
    mcfs_uniform_input = pickle.load(f)

with open(os.path.join(pkl_dir, 'input_cov_mcfs_Prob_5factor_40mins_open_flags_20230810_181953_484817.pkl'), 'rb') as f:
    mcfs_prob_input = pickle.load(f)

with open(os.path.join(pkl_dir, 'input_cov_mcfs_Inverse_Prob_5factor_40mins_sequence_pan_20230810_190452_580771.pkl'), 'rb') as f:
    mcfs_prob_inverse_input = pickle.load(f)

xfstests_open_flags = xfstests_input['open']['flags']
crashmonkey_open_flags = crashmonkey_input['open']['flags']
syzkaller_open_flags = syzkaller_input['open']['flags']
mcfs_uniform_open_flags = mcfs_uniform_input['open']['flags']
mcfs_prob_open_flags = mcfs_prob_input['open']['flags']
mcfs_prob_inverse_open_flags = mcfs_prob_inverse_input['open']['flags']

data1_crashmonkey = []
data2_xfstests = []
data3_syzkaller = []
data4_mcfs_uniform = []
data5_mcfs_prob = []
data6_mcfs_prob_inverse = []

x_labels = []

# print('xfstests_open_flags.keys(): ', xfstests_open_flags.keys())
# print('syzkaller_open_flags: ', syzkaller_open_flags)

ignored_flags = ['O_ACCMODE', 'O_RDONLY']

for open_flag in sorted(xfstests_open_flags.keys()):
    if open_flag not in ignored_flags:
        x_labels.append(open_flag)
        data1_crashmonkey.append(crashmonkey_open_flags[open_flag])
        data2_xfstests.append(xfstests_open_flags[open_flag])
        data3_syzkaller.append(syzkaller_open_flags[open_flag])
        data4_mcfs_uniform.append(mcfs_uniform_open_flags[open_flag])
        data5_mcfs_prob.append(mcfs_prob_open_flags[open_flag])
        data6_mcfs_prob_inverse.append(mcfs_prob_inverse_open_flags[open_flag])

data = np.array([data1_crashmonkey, data2_xfstests, data3_syzkaller, data4_mcfs_uniform, data5_mcfs_prob, data6_mcfs_prob_inverse])

# Numbers of open flags (x ticks)
N_open_flags = len(xfstests_open_flags.keys()) - len(ignored_flags)

# Position of bars on x-axis
x_pos = np.arange(N_open_flags)

labels = ['CrashMonkey', 'xfstests', 'Syzkaller', 'MCFS-Uniform', 'MCFS-Prob', 'MCFS-Prob-Inv']

# Determine the width and height in inches
width_inches = 9  # Example width for a two-column area
height_inches = 4 # Example height, adjust as needed

# Set up the plot
fig, ax = plt.subplots(figsize=(width_inches, height_inches))

# Width of a bar 
width = 0.1

ax.set_yscale('log')

ytick_values = [0.1, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
ytick_labels = ['0', '1', '10', '100', '1K', '10K', '100K', '1M', '10M']

plt.yticks(ytick_values, ytick_labels)

ax.set_ylim(ymin = 0.1)


ax.bar(x_pos - 5 * width / 2, data[0], width, color='#1f77b4', edgecolor='black', linewidth=0.5, label='CrashMonkey')
ax.bar(x_pos - 3 * width / 2, data[1], width, color='#ff7f0e',  edgecolor='black', linewidth=0.5, label='xfstests')
ax.bar(x_pos - width / 2, data[2], width, color='#2ca02c',  edgecolor='black', linewidth=0.5, label='Syzkaller')
ax.bar(x_pos + width / 2, data[3], width, color='#d62728',  edgecolor='black', linewidth=0.5, label='MCFS Uniform')
ax.bar(x_pos + 3 * width / 2, data[4], width, color='#9467bd',  edgecolor='black', linewidth=0.5, label='MCFS Prob')
ax.bar(x_pos + 5 * width / 2, data[5], width, color='#8c564b',  edgecolor='black', linewidth=0.5, label='MCFS Prob Inv')

ax.set_ylabel('Frequency (log scale base 10)', fontweight='bold')
ax.set_xlabel('Open Flags', fontweight='bold')

ax.legend(loc='best', ncol=len(labels))

ax.set_axisbelow(True)
ax.grid(axis='y', linestyle='-', alpha=0.3)

# print('x_labels: ', x_labels)
# plt.xticks(x_pos + width / 2, x_labels, rotation='vertical', fontsize=8)

plt.xticks(x_pos + width / 2, x_labels, rotation=45, ha='right', fontsize=8)

# Adjust the plot layout
plt.tight_layout()

# Save the plot to a PDF file as a vector plot
plt.savefig('fast24-input-open-flags.pdf', format='pdf', bbox_inches='tight')

#!/usr/bin/env python3

import statistics
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
from scipy.stats import gmean
import math

plt.rcParams["font.family"] = "Times New Roman"

# pkl_dir = '/mcfs2/LTTng-xfstests-2022-1211/IOCov/src'
pkl_dir = os.getcwd()

fig4_xfstests_input = {}
fig4_crashmonkey_input = {}
dpi_val = 600

with open(os.path.join(pkl_dir, 'fig4_input_cov_all_xfstests_xattrs.pkl'), 'rb') as f:
    fig4_xfstests_input = pickle.load(f)

with open(os.path.join(pkl_dir, 'fig4_input_cov_crashmonkey.pkl'), 'rb') as f:
    fig4_crashmonkey_input = pickle.load(f)

fig4_xfstests_open_flags = fig4_xfstests_input['open']['flags']
fig4_crashmonkey_open_flags = fig4_crashmonkey_input['open']['flags']

# print('fig4_xfstests_open_flags: ', fig4_xfstests_open_flags)
# print('fig4_crashmonkey_open_flags: ', fig4_crashmonkey_open_flags)

data1_crashmonkey = []
data2_xfstests = []

x_labels = []

# It is true for open flags
crashmonkey_subset_xfstests = True 

for open_flag in sorted(fig4_xfstests_open_flags.keys(), reverse=True):
    x_labels.append(open_flag)
    if fig4_xfstests_open_flags[open_flag] < fig4_crashmonkey_open_flags[open_flag]:
        crashmonkey_subset_xfstests = False
    data2_xfstests.append(fig4_xfstests_open_flags[open_flag])
    data1_crashmonkey.append(fig4_crashmonkey_open_flags[open_flag])

data = np.array([data1_crashmonkey, data2_xfstests])

# Numbers of pairs of bars you want
N_open_flags = len(fig4_xfstests_open_flags.keys())

# Position of bars on x-axis
ind = np.arange(N_open_flags)

labels = ['CrashMonkey', 'xfstests']
# Set up the plot
fig, ax = plt.subplots()

# Width of a bar 
width = 0.4

ax.set_yscale('log')

# set the tick locations and labels on the x-axis
# xtick_values = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
# xtick_labels = ['1', '10', '100', '1000', '10000', '100000', '1000000', '10000000']

ytick_values = [0.1, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
# xtick_labels = ['0', '1', '2', '3 (1K)', '4', '5', '6 (1M)', '7 (10M)']
ytick_labels = ['0', '1', '10', '100', '1K', '10K', '100K', '1M', '10M']

plt.yticks(ytick_values, ytick_labels)

ax.set_ylim(ymin = 0.1)

# Create the stacked bar chart
# 'green' 'orange'
ax.bar(ind, data[0], width, color='#4daf4a', edgecolor='black', linewidth=0.5, label='CrashMonkey')
ax.bar(ind + width, data[1], width, color='#ff7f0e',  edgecolor='black', linewidth=0.5, hatch='////', label='xfstests')

# Add a title and axis labels
# ax.set_title('Stacked Bar Chart')
ax.set_ylabel('Frequency (log scale base 10)', fontweight='bold')
ax.set_xlabel('Open Flags', fontweight='bold')

# Add a legend
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=len(labels))
ax.legend(loc='best', ncol=len(labels))

ax.set_axisbelow(True)
ax.grid(axis='y', linestyle='-', alpha=0.3)

# print('x_labels: ', x_labels)
plt.xticks(ind + width / 2, x_labels, rotation='vertical', fontsize=8)

# Adjust the plot layout
plt.tight_layout()

# Save the plot to a PDF file as a vector plot
plt.savefig('crc-input-open-flags.pdf', format='pdf', bbox_inches='tight')

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
figure_dir = '/mcfs/iocov-mcfs-fast24-2023-0723/IOCov/FAST2024/expts-figures'
figure_file_name = 'only-metis-input-open-flags.pdf'

all_open_flags = []
pkl_files = [
    'input-cov-mcfs-Uniform-50p-40mins-open-flags-20230905-003428-1106728.pkl', # Uniform 50%
    'input-cov-mcfs-RZD-40mins-open-flags-20230904-033012-1045713.pkl', # Rank-size distribution 
    'input-cov-mcfs-RZD-inverse-40mins-open-flags-20230904-042627-1069081.pkl' # Inverse Rank-size distribution 
    ]
num_tools = len(pkl_files)
for i in range(num_tools):
    with open(os.path.join(pkl_dir, pkl_files[i]), 'rb') as f:
        input_data = pickle.load(f)
        all_open_flags.append(input_data['open']['flags'])


# print('all_open_flags: ', all_open_flags)

x_labels = []

# print('xfstests_open_flags.keys(): ', xfstests_open_flags.keys())
# print('syzkaller_open_flags: ', syzkaller_open_flags)

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

# print('x_labels: ', x_labels)
# print('all_data: ', all_data)
# print('all_data_arr: ', all_data_arr)
# print('===============================')

# Numbers of open flags (x ticks)
N_open_flags = len(all_open_flags[0].keys()) - len(ignored_flags)

# Position of bars on x-axis
x_pos = np.arange(N_open_flags)

# Determine the width and height in inches
width_inches = 9  # Example width for a two-column area
height_inches = 4 # Example height, adjust as needed

# Set up the plot
fig, ax = plt.subplots(figsize=(width_inches, height_inches))

# Width of a bar 
width = 0.2

# ax.set_yscale('log')
# ytick_values = [0.1, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
# ytick_labels = ['0', '1', '10', '100', '1K', '10K', '100K', '1M', '10M']
# plt.yticks(ytick_values, ytick_labels)
# ax.set_ylim(ymin = 0.1)

# print('all_data_arr: ', all_data_arr)

# Plot the data
bar_coords = [x_pos - width, x_pos, x_pos + width]
bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
edgecolors = ['black', 'black', 'black']
linewidths = [0.5, 0.5, 0.5]
labels = ['Metis Uniform', 'Metis RSD', 'MCFS IRSD'] # IRSD: Inverse Rank-size distribution 

for i in range(num_tools):
    ax.bar(bar_coords[i], all_data_arr[i], width, color=bar_colors[i], edgecolor=edgecolors[i], linewidth=linewidths[i], label=labels[i])

ax.set_ylabel('Frequency (number of inputs tested)', fontweight='bold')
ax.set_xlabel('Open Flags', fontweight='bold')

# ax.legend(loc='best', ncol=len(labels))
ax.legend(fontsize='small', loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=len(labels))

ax.set_axisbelow(True)
ax.grid(axis='y', linestyle='-', alpha=0.3)

# print('x_labels: ', x_labels)
# plt.xticks(x_pos + width / 2, x_labels, rotation='vertical', fontsize=8)

plt.xticks(x_pos + width / 2, x_labels, rotation=45, ha='right', fontsize=8)

# Adjust the plot layout
plt.tight_layout()

# Save the plot to a PDF file as a vector plot
plt.savefig(os.path.join(figure_dir, figure_file_name), format='pdf', bbox_inches='tight')

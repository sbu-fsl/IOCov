#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import sys
sys.path.append('../src')
from utilities import *
from matplotlib.ticker import ScalarFormatter
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

sole_label = 'write-size-Metis-Uniform-40mins'
sole_pkl_file = ''

if len(sys.argv) == 3:
    sole_label = sys.argv[1]
    sole_pkl_file = sys.argv[2]
    print(f"Label (arg1): {sole_label}")
    print(f"Input coords pickle file path (arg2): {sole_pkl_file}")
else:
    sys.exit("Please provide exactly two arguments.")

labels = [sole_label]
coord_pkl_files = [sole_pkl_file]

# labels = ['Metis-Uniform', 'Metis-XD', 'Metis-IXD'] # IRSD: Inverse Rank-size distribution

# coord_pkl_files = ['mcfs-Uniform-4hours-write-sizes-20230907-001716-1330916_input_coords.pkl', # Metis Uniform 50%
#                   'mcfs-RZDN-90p-4hours-write-sizes-20230907-042128-1421507_input_coords.pkl', # Metis RZDN 90%
#                   'mcfs-IRZD-4hours-33parts-90p-write-size-20230907-203157-1594068_input_coords.pkl' # Metis RZDN Inverse 90%
#                   ]

figure_file_name = 'metis-{}.pdf'.format(sole_label)

width = 0.2

# Key: testing tool (in labels)
# Value: list of X and Y coordinates for the corresponding testing tool
all_axes = {}

for i in range(len(coord_pkl_files)):
    X_tests, Y_tests = read_write_count_by_pkl(os.getcwd(), coord_pkl_files[i])
    all_axes[labels[i]] = [X_tests, Y_tests]

x_labels = all_axes[labels[0]][0]

Y_data = []

for i in range(len(labels)):
    Y_data.append(all_axes[labels[i]][1])

Y_data = np.array(Y_data)

# Determine the width and height in inches
width_inches = 5  # Example width for a two-column area
height_inches = 2 # Example height, adjust as needed

# Set up the plot
fig, ax = plt.subplots(figsize=(width_inches, height_inches))

# Position of bars on x-axis
x_pos = np.arange(len(all_axes[labels[0]][0]))

x_pos = x_pos[:-1]
x_labels = x_labels[:-1]

ytick_values = [0, 30, 60, 90, 120, 150]
ytick_labels = ['0', '30', '60', '90', '120', '150']

bar_coords = [x_pos]
bar_colors = ['#FF3333']
edgecolors = ['black']
linewidths = [0.5]

# Plot the bars for each testing tool
for i in range(len(bar_coords)):
    ax.bar(bar_coords[i], Y_data[i][:-1], width, color=bar_colors[i], edgecolor=edgecolors[i], linewidth=linewidths[i], label=labels[i])

x_first_label = x_labels[0]
x_labels[0] = ''

ax.set_xticks(x_pos + width / 2, x_labels, ha='center', fontsize=8)

# print('x_pos[1::2]: ', x_pos[1::2])
# print('x_labels[1::2]]: ', x_labels[1::2])

x_first_label = 'Equals 0'

plt.xticks(x_pos)

new_labels = ['' if i % 2 == 0 else label for i, label in enumerate(x_labels)]
new_labels[0] = x_first_label
xticks_toset = plt.gca().set_xticklabels(new_labels)

xticks_toset[0].set_rotation(20)
xticks_toset[0].set_ha('right')
xticks_toset[0].set_fontsize(8)

# Create a function to define the transformation
def transform(x):
    return x  # Example transformation for secondary x-axis

# Set secondary x-axis values
secx = ax.secondary_xaxis('top', functions=(transform, transform))

sec_xtick_gap = 4

sec_x_pos_list = []

for i in range(len(x_pos)):
    if i == 0:
        sec_x_pos_list.append(x_pos[i])
    elif i % sec_xtick_gap == 1:
        sec_x_pos_list.append(x_pos[i])

sec_x_pos = np.array(sec_x_pos_list)

secx.set_xticks(sec_x_pos + width / 2)

def number_to_bytes(num):
    res_num = 2 ** num
    if res_num < 1024:
        return f'{res_num}B'
    elif res_num < 1024 ** 2:
        return f'{int(res_num / 1024)}KiB'
    elif res_num < 1024 ** 3:
        return f'{int(res_num / 1024 ** 2)}MiB'
    elif res_num < 1024 ** 4:
        return f'{int(res_num / 1024 ** 3)}GiB'

second_x_labels = []
for i in range(len(x_labels)):
    if i == 0:
        second_x_labels.append('0B')
    elif i % sec_xtick_gap == 1:
        second_x_labels.append(number_to_bytes(int(x_labels[i])))

secx.set_xticklabels(second_x_labels, fontsize=8)

plt.yticks(ytick_values, ytick_labels)

ax.set_ylim(ymin = 0.1)

ax.set_ylabel('Count', fontweight='bold', fontsize=10)

ax.legend(fontsize=8, loc='best', ncol=len(labels))

ax.set_axisbelow(True)
ax.grid(axis='y', linestyle='dotted', alpha=0.4)
ax.grid(axis='x', linestyle='dotted', alpha=0.4)

# Adjust the plot layout
plt.tight_layout()

fig.savefig(figure_file_name, format='pdf', bbox_inches='tight')

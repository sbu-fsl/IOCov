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

plt.rcParams["font.family"] = "Times New Roman"

dpi_val = 600

pkl_dir = '/mcfs/iocov-mcfs-fast24-2023-0723/IOCov/FAST2024/input-pickles'

labels = ['Metis Uniform', 'Metis RSD', 'Metis IRSD'] # IRSD: Inverse Rank-size distribution

coord_pkl_files = ['mcfs-Uniform-4hours-write-sizes-20230907-001716-1330916_input_coords.pkl', # Metis Uniform 50%
                   'mcfs-RZDN-90p-4hours-write-sizes-20230907-042128-1421507_input_coords.pkl', # Metis RZDN 90%
                   'mcfs-IRZD-4hours-33parts-90p-write-size-20230907-203157-1594068_input_coords.pkl' # Metis RZDN Inverse 90%
                   ]

figure_dir = '/mcfs/iocov-mcfs-fast24-2023-0723/IOCov/FAST2024/expts-figures'
figure_file_name = 'only-metis-input-write-sizes-4hours.pdf'

width = 0.2

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

# Determine the width and height in inches
width_inches = 9  # Example width for a two-column area
height_inches = 4 # Example height, adjust as needed

# Set up the plot
fig, ax = plt.subplots(figsize=(width_inches, height_inches))

# Position of bars on x-axis
x_pos = np.arange(len(all_axes[labels[0]][0]))

x_pos = x_pos[:-1]
x_labels = x_labels[:-1]

#print('x_pos: ', x_pos)
#print('x_labels: ', x_labels)

plt.xticks(x_pos, x_labels)

# ax.set_yscale('log')

# ytick_values = [0, 20, 40, 60, 80, 100]
# ytick_labels = ['0', '20', '40', '60', '80', '100']

ytick_values = [0, 200, 400, 600, 800, 1000]
ytick_labels = ['0', '200', '400', '600', '800', '1000']

bar_coords = [x_pos - width, x_pos, x_pos + width]
bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
edgecolors = ['black', 'black', 'black']
linewidths = [0.5, 0.5, 0.5]
labels = ['Metis Uniform', 'Metis RSD', 'MCFS IRSD'] # IRSD: Inverse Rank-size distribution 

# Plot the bars for each testing tool
for i in range(len(bar_coords)):
    ax.bar(bar_coords[i], Y_data[i][:-1], width, color=bar_colors[i], edgecolor=edgecolors[i], linewidth=linewidths[i], label=labels[i])

x_first_label = x_labels[0]
x_labels[0] = ''

ax.set_xticks(x_pos + width / 2, x_labels, rotation=45, ha='center', fontsize=8)
ax.text(width / 2, 0.005, x_first_label, rotation=45, ha='right', fontsize=8)

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

# print('sec_x_pos: ', sec_x_pos)
# print('second_x_labels: ', second_x_labels)
secx.set_xticklabels(second_x_labels, fontsize=8)

plt.yticks(ytick_values, ytick_labels)

ax.set_ylim(ymin = 0.1)

#ax.set_title('My Bar Chart')
ax.set_xlabel('Write Size in Bytes (exponent of log base 2)', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')

# Add a legend
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=len(labels))
# ax.legend(loc='best', ncol=len(labels))
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.16), ncol=len(labels))
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=len(labels))

ax.set_axisbelow(True)
ax.grid(axis='y', linestyle='dotted', alpha=0.4)
ax.grid(axis='x', linestyle='dotted', alpha=0.4)

# Adjust the plot layout
plt.tight_layout()

# dpi=dpi_val
fig.savefig(os.path.join(figure_dir, figure_file_name), format='pdf', bbox_inches='tight')

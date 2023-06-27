#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
from matplotlib.ticker import ScalarFormatter
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import sys

plt.rcParams["font.family"] = "Times New Roman"

pkl_dir = os.getcwd()

def read_write_count_by_pkl(pkl_file):
    fig5_xfstests_input_coords = {}

    with open(os.path.join(pkl_dir, pkl_file), 'rb') as f:
        fig5_xfstests_input_coords = pickle.load(f)

    xfstests_write_count = fig5_xfstests_input_coords['write']['count']

    X_xfstests = xfstests_write_count['X-axis']
    Y_xfstests = xfstests_write_count['Y-axis']

    # print('xfstests_write_count: ', xfstests_write_count)
    """
    print('len(X_xfstests): ', len(X_xfstests))
    for i in range(len(X_xfstests) - 1, -1, -1):
        if Y_xfstests[i] > 0:
            print('i: ', i)
            print('X_xfstests: ', X_xfstests[i])
            break
    """
    Keep = -1
    for i in range(len(X_xfstests)):
        each_X = X_xfstests[i]
        if each_X == '2^32':
            Keep = i 

    # Labels
    X_cut_xfstests = X_xfstests[0:Keep+1]
    # Real Values
    Y_cut_xfstests = Y_xfstests[0:Keep+1]

    # print('X_cut_xfstests: ', X_cut_xfstests)
    # print('Y_cut_xfstests: ', Y_cut_xfstests)

    # ROUND DOWN: 2^{10} == 1024 (1024 - 2047)
    X_xfstests = []
    Y_xfstests = []
    
    for i in range(len(X_cut_xfstests)):
        if X_cut_xfstests[i] == 'Intv.':
            Y_xfstests[-1] += Y_cut_xfstests[i]
        else: # Not 'Intv.'
            X_xfstests.append(X_cut_xfstests[i])
            Y_xfstests.append(Y_cut_xfstests[i])

    """
    # ONLY BOUNDARY VALUES EXACTLY EQUAL TO POWERS OF 2 NUMBERS
    X_xfstests = []
    Y_xfstests = []
    for i in range(len(X_cut_xfstests)):
        if X_cut_xfstests[i] != 'Intv.':
            X_xfstests.append(X_cut_xfstests[i])
            Y_xfstests.append(Y_cut_xfstests[i])

    X_xfstests.pop(0)
    Y_xfstests.pop(0)
    # print('X_xfstests: ', X_xfstests)
    # print('Y_xfstests: ', Y_xfstests)
    """
    # Do not use 2^10, use 10 instead 
    for i in range(len(X_xfstests)):
        X_xfstests[i] = X_xfstests[i].split('^')[-1]
    
    X_xfstests[0] = 'Equal to 0'
    return X_xfstests, Y_xfstests


xfstests_pkl_file = 'fig5_xfstests_input_coords.pkl'
crashmonkey_pkl_file = 'fig5_crashmonkey_input_coords.pkl'

X_xfstests, Y_xfstests = read_write_count_by_pkl(xfstests_pkl_file)
X_crashmonkey, Y_crashmonkey = read_write_count_by_pkl(crashmonkey_pkl_file)

# print('X_xfstests: ', X_xfstests)
# print('Y_xfstests: ', Y_xfstests)

# print('X_crashmonkey: ', X_crashmonkey)
# print('Y_crashmonkey: ', Y_crashmonkey)

x_labels = X_xfstests

Y_data = np.array([Y_crashmonkey, Y_xfstests])

labels = ['CrashMonkey', 'xfstests']

### Plotting 
# fig, ax = plt.subplots(figsize=(10, 6))
fig, ax = plt.subplots()

# Position of bars on x-axis
x_pos = np.arange(len(X_xfstests))

width = 0.35

plt.xticks(x_pos, X_xfstests)
ax.set_yscale('log')

ytick_values = [0.1, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
# ytick_labels = ['0', '1', '2', '3 (1K)', '4', '5', '6 (1M)', '7 (10M)']
ytick_labels = ['0', '1', '10', '100', '1K', '10K', '100K', '1M', '10M']

# 'maroon', ['#77b5e5' (blue), '#4daf4a' (green), '#f0e442' (yellow), '#d62728' (red), '#984ea3' (purple), '#ff7f0e' (orange)]
# ax.barh(x_pos, Y_xfstests, log=True, color ='#77b5e5', edgecolor='black', linewidth=0.5)

# print('x_pos: ', x_pos)
# print('Y_data[0]: ', Y_data[0])
# print('Y_data[1]: ', Y_data[1])

ax.bar(x_pos, Y_data[0], width, color='#4daf4a', edgecolor='black', linewidth=0.5, hatch='//', label='CrashMonkey')
ax.bar(x_pos + width, Y_data[1], width, color='#ff7f0e',  edgecolor='black', linewidth=0.5, label='xfstests')

# annotation for the max write size bar
arrow_x = 28
arrow_y = 1

# print('arrow_x: ', arrow_x)
# print('arrow_y: ', arrow_y)

annotation_text = f'Max 258 MiB'  # annotation text

plt.annotate(annotation_text, xy=(arrow_x + 1.25 + width/4, arrow_y), xytext=(arrow_x + 1.25 + width/4, arrow_y + 5),
             arrowprops=dict(color='black', arrowstyle='->'), ha='center', fontsize=8, color='black')

# plt.xlim(left=0.1)
# print('x_pos: ', x_pos)
# print('x_labels: ', x_labels)
# print('width: ', width)

x_first_label = x_labels[0]
x_labels[0] = ''

# ax.set_xticks(x_pos[:1] + width / 2, x_labels[:1], rotation=45, ha='right', fontsize=8)
ax.set_xticks(x_pos + width / 2, x_labels, rotation=45, ha='center', fontsize=8)
# ax.set_xticks(x_pos + width / 2, x_labels, rotation=45, ha='center', fontsize=8)
ax.text(width / 2, 0.012, x_first_label, rotation=45, ha='right', fontsize=8)

# Create a function to define the transformation
def transform(x):
    return x  # Example transformation for secondary x-axis

# Set secondary x-axis values
secx = ax.secondary_xaxis('top', functions=(transform, transform))

# primary_xticks = ax.get_xticks()
# secx.set_xticks(primary_xticks)
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
ax.set_xlabel('Write Size in Bytes (log base 2)', fontweight='bold')
ax.set_ylabel('Frequency (log scale base 10)', fontweight='bold')

# Add a legend
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=len(labels))
ax.legend(loc='best', ncol=len(labels))
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.16), ncol=len(labels))

ax.set_axisbelow(True)
ax.grid(axis='y', linestyle='dotted', alpha=0.4)
ax.grid(axis='x', linestyle='dotted', alpha=0.4)

# Adjust the plot layout
plt.tight_layout()

# dpi=dpi_val
dpi_val = 600
fig.savefig('slides-input-write-size.png', format='png', bbox_inches='tight', dpi=dpi_val)

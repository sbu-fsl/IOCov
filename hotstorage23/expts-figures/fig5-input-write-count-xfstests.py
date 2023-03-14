#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
from matplotlib.ticker import ScalarFormatter

dpi_val = 600

plt.rcParams["font.family"] = "Times New Roman"

pkl_dir = os.getcwd()

fig5_xfstests_input_coords = {}

with open(os.path.join(pkl_dir, 'fig5_xfstests_input_coords.pkl'), 'rb') as f:
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

X_xfstests = []
Y_xfstests = []
for i in range(len(X_cut_xfstests)):
    if X_cut_xfstests[i] != 'Intv.':
        X_xfstests.append(X_cut_xfstests[i])
        Y_xfstests.append(Y_cut_xfstests[i])

X_xfstests.pop(0)
Y_xfstests.pop(0)
print('X_xfstests: ', X_xfstests)
print('Y_xfstests: ', Y_xfstests)

# Do not use 2^10, use 10 instead 
for i in range(len(X_xfstests)):
    X_xfstests[i] = X_xfstests[i].split('^')[-1]

# print('X_xfstests: ', X_xfstests)
# print('Y_xfstests: ', Y_xfstests)

### Plotting 
fig, ax = plt.subplots(figsize=(10, 6))

y_pos = np.arange(len(X_xfstests))
plt.yticks(y_pos, X_xfstests)

xtick_values = [0.1, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
# xtick_labels = ['0', '1', '2', '3 (1K)', '4', '5', '6 (1M)', '7 (10M)']
xtick_labels = ['0', '1', '10', '100', '1K', '10K', '100K', '1M', '10M']

# 'maroon', ['#77b5e5' (blue), '#4daf4a' (green), '#f0e442' (yellow), '#d62728' (red), '#984ea3' (purple), '#ff7f0e' (orange)]
ax.barh(y_pos, Y_xfstests, log=True, color ='#77b5e5', edgecolor='black', linewidth=0.5)
# plt.xlim(left=0.1)

ax.set_yticks(ax.get_yticks()[::2])

plt.xticks(xtick_values, xtick_labels)

ax.set_xlim(xmin = 0.1)

# Set the arrow
arrow_index = 26
arrow_x = Y_xfstests[arrow_index]
arrow_y = y_pos[arrow_index]
arrow_text = f'Max write size 258 MiB'
ax.annotate(arrow_text, xy=(arrow_x, arrow_y), xytext=(arrow_x+5, arrow_y),
             arrowprops=dict(facecolor='red', arrowstyle='->'))

#ax.set_title('My Bar Chart')
ax.set_xlabel('Frequency (log scale base 10)', fontweight='bold')
ax.set_ylabel('Write Size in Bytes (exponent of log base 2)', fontweight='bold')

# dpi=dpi_val
fig.savefig('fig5-write-count-xfstests.pdf', format='pdf', bbox_inches='tight')

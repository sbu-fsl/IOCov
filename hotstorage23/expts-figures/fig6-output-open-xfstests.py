#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import os
import pickle

plt.rcParams["font.family"] = "Times New Roman"

# pkl_dir = '/mcfs2/LTTng-xfstests-2022-1211/IOCov/src'
pkl_dir = os.getcwd()
fig6_xfstests_output = {}

dpi_val = 600
sc = 'open'

# errors_dict = {}
# with open(os.path.join(pkl_dir, 'errors_dict.pkl'), 'rb') as f:
#    errors_dict = pickle.load(f)

with open(os.path.join(pkl_dir, 'xfstests_xattr_open_dump_output_coords.pkl'), 'rb') as f:
    fig6_xfstests_output = pickle.load(f)

xaxis = fig6_xfstests_output[sc]['X-axis']
yaxis = fig6_xfstests_output[sc]['Y-axis']

xaxis.reverse()
yaxis.reverse()

# print('xaxis: ', xaxis)
# print('yaxis: ', yaxis)

# print('type(xaxis): ', type(xaxis))
# print('type(yaxis): ', type(yaxis))

fig, ax = plt.subplots(figsize=(8, 6))

xtick_values = [0.1, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
xtick_labels = ['0', '1', '10', '100', '1K', '10K', '100K', '1M', '10M']

# 'maroon'
ax.barh(xaxis, yaxis, log=True, color ='#d62728', edgecolor='black', linewidth=0.5)

plt.xticks(xtick_values, xtick_labels)

# plt.xlim(left=0.1)
ax.set_xlim(xmin = 0.1)

ax.set_xlabel('Frequency (log scale base 10)', fontweight='bold')
ax.set_ylabel('Open Return and Error', fontweight='bold')

fig.savefig('fig6-open-return-xfstests.pdf', format='pdf', bbox_inches='tight')

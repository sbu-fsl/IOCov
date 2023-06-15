#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

plt.rcParams["font.family"] = "Times New Roman"

# pkl_dir = '/mcfs2/LTTng-xfstests-2022-1211/IOCov/src'
pkl_dir = os.getcwd()
fig6_xfstests_output = {}

sc_name = 'open'

# errors_dict = {}
# with open(os.path.join(pkl_dir, 'errors_dict.pkl'), 'rb') as f:
#    errors_dict = pickle.load(f)
def read_output_coords_by_pkl(sc, pkl_file):
    with open(os.path.join(pkl_dir, pkl_file), 'rb') as f:
        fig6_xfstests_output = pickle.load(f)

    xaxis = fig6_xfstests_output[sc]['X-axis']
    yaxis = fig6_xfstests_output[sc]['Y-axis']

    xaxis.reverse()
    yaxis.reverse()
    return xaxis, yaxis

xfstest_pkl_file = 'xfstests_xattr_open_dump_output_coords.pkl'
crashmonkey_pkl_file = 'crashmonkey_output_coords.pkl'

xfstest_xaxis, xfstest_yaxis = read_output_coords_by_pkl(sc_name, xfstest_pkl_file)
crashmonkey_xaxis, crashmonkey_yaxis = read_output_coords_by_pkl(sc_name, crashmonkey_pkl_file)

# print('xfstest_xaxis: ', xfstest_xaxis)
# print('xfstest_yaxis: ', xfstest_yaxis)

# print('crashmonkey_xaxis: ', crashmonkey_xaxis)
# print('crashmonkey_yaxis: ', crashmonkey_yaxis)

# print('type(xaxis): ', type(xaxis))
# print('type(yaxis): ', type(yaxis))

# xfstests is SMALLER than crashmonkey:  7 ENOTDIR
# for i in range(len(xfstest_yaxis)):
#     if xfstest_yaxis[i] < crashmonkey_yaxis[i]:
#         print('xfstests is SMALLER than crashmonkey: ', i, xfstest_xaxis[i])

Y_data = np.array([crashmonkey_yaxis, xfstest_yaxis])

labels = ['CrashMonkey', 'xfstests']

# fig, ax = plt.subplots(figsize=(8, 6))
fig, ax = plt.subplots()

width = 0.5

x_pos = np.arange(len(xfstest_xaxis))

ax.set_yscale('log')

ytick_values = [0.1, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
ytick_labels = ['0', '1', '10', '100', '1K', '10K', '100K', '1M', '10M']

# 'maroon'
# ax.barh(xaxis, yaxis, log=True, color ='#d62728', edgecolor='black', linewidth=0.5)
xfstest_xaxis[0] = 'OK (>= 0)'

x_labels = xfstest_xaxis

ax.bar(x_pos, Y_data[0], width, color='#4daf4a', edgecolor='black', linewidth=0.5, hatch='//', label='CrashMonkey')
ax.bar(x_pos + width, Y_data[1], width, color='#ff7f0e',  edgecolor='black', linewidth=0.5, label='xfstests')

plt.yticks(ytick_values, ytick_labels)

plt.xticks(x_pos + width / 2, x_labels, rotation=45, ha='right', fontsize=8)

# plt.xlim(left=0.1)
ax.set_ylim(ymin = 0.1)

ax.set_ylabel('Frequency (log scale base 10)', fontweight='bold')
ax.set_xlabel('Open Return Code or Error', fontweight='bold')

# ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=len(labels))
ax.legend(loc='best', ncol=len(labels))

ax.set_axisbelow(True)
ax.grid(axis='y', linestyle='-', alpha=0.3)

plt.tight_layout()

dpi_val = 600
fig.savefig('crc-output-open.pdf', format='pdf', bbox_inches='tight', dpi=dpi_val)

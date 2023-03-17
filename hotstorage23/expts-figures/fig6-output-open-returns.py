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

diff_yaxis = []
for i in range(len(xfstest_xaxis)):
    if xfstest_yaxis[i] >= crashmonkey_yaxis[i]:
        diff_yaxis.append(xfstest_yaxis[i] - crashmonkey_yaxis[i])
    else:
        diff_yaxis.append(crashmonkey_yaxis[i] - xfstest_yaxis[i])

Y_data = np.array([crashmonkey_yaxis, diff_yaxis])

labels = ['CrashMonkey', 'xfstests']

# fig, ax = plt.subplots(figsize=(8, 6))
fig, ax = plt.subplots()

ax.set_xscale('log')

xtick_values = [0.1, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
xtick_labels = ['0', '1', '10', '100', '1K', '10K', '100K', '1M', '10M']

# 'maroon'
# ax.barh(xaxis, yaxis, log=True, color ='#d62728', edgecolor='black', linewidth=0.5)
xfstest_xaxis[0] = 'OK (>= 0)'

crashmonkey_bars = ax.barh(xfstest_xaxis, Y_data[0], color='#4daf4a', edgecolor='black', linewidth=0.5, label='CrashMonkey')
diff_bars = ax.barh(xfstest_xaxis, Y_data[1], color='#ff7f0e',  edgecolor='black', linewidth=0.5, left=Y_data[0], hatch='////', label='xfstests')

diff_idx = 7

crashmonkey_bars[diff_idx].set_facecolor('#ff7f0e')
crashmonkey_bars[diff_idx].set_hatch('////')
diff_bars[diff_idx].set_facecolor('#4daf4a')
# Set as no hatch
diff_bars[diff_idx].set_hatch('')

plt.xticks(xtick_values, xtick_labels)

# plt.xlim(left=0.1)
ax.set_xlim(xmin = 0.1)

ax.set_xlabel('Frequency (log scale base 10)', fontweight='bold')
ax.set_ylabel('Open Return Code or Error', fontweight='bold')

ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=len(labels))

plt.tight_layout()

fig.savefig('fig6-open-return.pdf', format='pdf', bbox_inches='tight')

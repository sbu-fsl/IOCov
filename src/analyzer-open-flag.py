#!/usr/bin/env python3

import pickle
import json
from constants import *
import matplotlib.pyplot as plt
import numpy as np
import sys 

# Distribution of the specific open flag (e.g., O_CREAT 0o100)
creat_flag = 0o100

# Plot
sort_legend = True
plot_dpi = 600

# open_flag_unfilter = {}
# with open('open_flag_unfilter.pkl', 'rb') as f:
#    open_flag_unfilter = pickle.load(f)

open_flag_filtered = {}

with open('open_flag_filtered.pkl', 'rb') as f:
    open_flag_filtered = pickle.load(f)

"""
with open('open_flag_unfilter.json', 'w') as fout:
    open_flag_unfilter_str = json.dumps(open_flag_unfilter, indent=4)
    print(open_flag_unfilter_str, file=fout)
with open('open_flag_filtered.json', 'w') as fout:
    open_flag_filtered_str = json.dumps(open_flag_filtered, indent=4)
    print(open_flag_filtered_str, file=fout)
"""

all_cnt_res = {}
creat_cnt_res = {}

# Distribution of ALL open flags
for flag, cnt in open_flag_filtered.items():
    flag_num = bin(flag).count("1")
    # #define O_RDONLY	00000000
    if flag & 1 == 0:
        flag_num += 1
    if flag_num in all_cnt_res.keys():
        all_cnt_res[flag_num] += cnt
    else:
        all_cnt_res[flag_num] = cnt     
    # if O_CREAT is enabled
    if flag & creat_flag == creat_flag:
        if flag_num in creat_cnt_res.keys():
            creat_cnt_res[flag_num] += cnt
        else:
            creat_cnt_res[flag_num] = cnt

# Plot all open flags and open flags that contain O_CREAT
res_list = [all_cnt_res, creat_cnt_res]
title_list = ['all', 'O_CREAT']
for i in range(len(res_list)):
    each_res = res_list[i]
    y_all_list = []
    all_labels = []
    for flag_num, cnt in each_res.items():
        y_all_list.append(cnt)
        all_labels.append(str(flag_num))

    y_all = np.asarray(y_all_list)
    all_percents = 100.*y_all/y_all.sum()

    all_labels = ['{0} flags ({1:1.2f} %)'.format(i,j) for i,j in zip(all_labels, all_percents)]

    patches, texts = plt.pie(y_all, startangle=90)

    if sort_legend:
        patches, all_labels, dummy =  zip(*sorted(zip(patches, all_labels, y_all),
                                            key=lambda x: x[2],
                                            reverse=True))

    plt.legend(patches, all_labels, loc='best', bbox_to_anchor=(-0.1, 1.),
            fontsize=8)

    plt.title('Number of flags (bits) for open {} [xfstests ext4 all, filtered]'.format(title_list[i]))
    plt.savefig('./Assets/Analysis-Figures/filtered-open-flags-{}.pdf'.format(title_list[i]), bbox_inches='tight',dpi=plot_dpi)
    plt.close('all')

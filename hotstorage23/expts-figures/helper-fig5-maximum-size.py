#!/usr/bin/env python3

import pickle
import os

pkl_dir = os.getcwd()

with open(os.path.join(pkl_dir, 'fig4_input_cov_all_xfstests_xattrs.pkl'), 'rb') as f:
    xfstests_input = pickle.load(f)

# print('xfstests_input: ', xfstests_input['write']['count'])

# Maximum xfstests write size: 270532608 258MiB
# print('xfstests_input: ', max(xfstests_input['write']['count'].keys()))

fig5_xfstests_input_coords = {}

with open(os.path.join(pkl_dir, 'fig5_xfstests_input_coords.pkl'), 'rb') as f:
    fig5_xfstests_input_coords = pickle.load(f)

xfstests_write_count = fig5_xfstests_input_coords['write']['count']

X_xfstests = xfstests_write_count['X-axis']
Y_xfstests = xfstests_write_count['Y-axis']

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

for i in range(len(X_xfstests) - 1, -1, -1):
    if Y_xfstests[i] > 0:
        print('i: ', i)
        print('X_xfstests: ', X_xfstests[i])
        break

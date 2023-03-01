#!/usr/bin/env python3

import pickle

sc_args = {'open': 'mode', 
            'read': 'count',
            'write': 'count',
            'lseek': 'whence',
            'truncate': 'length',
            'mkdir': 'mode',
            'chmod': 'mode'
            }

unfilter_input_cov = {}
input_cov = {}
save_ratio = {}

with open('unfilter_input_cov_chdir.pkl', 'rb') as f:
    unfilter_input_cov = pickle.load(f)
with open('input_cov_chdir.pkl', 'rb') as f:
    input_cov = pickle.load(f)

unfilter_count = {}
filtered_count = {}

for sc in sc_args.keys():
    unfilter_count[sc] = 0
    filtered_count[sc] = 0

for sc, arg in sc_args.items():
    unfilter_vals = unfilter_input_cov[sc][arg]
    filtered_vals = input_cov[sc][arg]
    for val in unfilter_vals.values():
        unfilter_count[sc] += val 
    for val in filtered_vals.values():
        filtered_count[sc] += val 

# print('unfilter_count: ', unfilter_count)
# print('filtered_count: ', filtered_count)
for sc in sc_args.keys():
    save_ratio[sc] = (unfilter_count[sc] - filtered_count[sc]) / filtered_count[sc]

print('save_ratio: ', save_ratio)

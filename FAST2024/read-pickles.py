#!/usr/bin/env python3

import pickle
import json
import os

plk_files = ['fig4_input_cov_all_xfstests_xattrs.pkl', 
             'fig4_input_cov_crashmonkey.pkl', 
             'input_cov_syzkaller_40mins_2023_0809_0037.pkl',
             'fig5_crashmonkey_input_coords.pkl', 
             'fig5_xfstests_input_coords.pkl',
             'syzkaller_40mins_2023_0809_0037_input_coords.pkl',
             'input_cov_mcfs_Uniform_50p_40mins_open_flags_20230810_170456_382883.pkl',
             'input_cov_mcfs_Prob_5factor_40mins_open_flags_20230810_181953_484817.pkl',
             'input_cov_mcfs_Inverse_Prob_5factor_40mins_sequence_pan_20230810_190452_580771.pkl',
             'input_cov_mcfs_Uniform_40mins_write_sizes_20230812_213410_786070.pkl',
             'mcfs_Uniform_40mins_write_sizes_20230812_213410_786070_input_coords.pkl']

plk_dir = '/mcfs/iocov-mcfs-fast24-2023-0723/IOCov/FAST2024/input-pickles'

for plk_file in plk_files:
    # Load data from pickle file
    with open(os.path.join(plk_dir, plk_file), 'rb') as pkl_file:
        data = pickle.load(pkl_file)

    # Save data to JSON file with indentation
    with open(os.path.join(plk_dir, plk_file.split('.')[0] + '.json'), 'w') as json_file:
        json.dump(data, json_file, indent=4)  # The number 4 here represents the number of spaces for indentation

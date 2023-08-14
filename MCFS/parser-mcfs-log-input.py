#!/usr/bin/env python3

import json
import pickle
import sys
# Make sure you are in MCFS folder
sys.path.append('../src')
from constants import *
from utilities import *

name_suffix = 'Uniform-40mins-write-sizes-20230812-213410-786070'

# TODO: for multiple sequence files, we need to combine them and analyze them together
seq_log = 'Uniform-40mins-write-sizes-sequence-pan-20230812-213410-786070.log'

# key: base-syscall
# value: a dict 
### key: each argument name of the base-syscall and its variants
### value: a dict
##### key: each input partition 
##### value: frequency of each input partition
all_input_cov = init_input_cov()

all_open_flags = []
all_open_mode = []
all_lseek_offset = []
all_write_count = []
all_truncate_length = []
all_mkdir_mode = []
all_chmod_mode = []
all_setxattr_size = []
all_setxattr_flags = []

with open(seq_log, 'r', encoding="utf8", errors='ignore') as file:
    lines = file.readlines()
    for line in lines:
        ops_name = line.split(',')[0]
        if ops_name == 'checkpoint' or ops_name == 'restore':
            continue
        # create_file: open flags, open mode
        elif ops_name == 'create_file':
            # open flags
            open_flag = int(line.split(',')[2]) # save open flag as decimal
            all_open_flags.append(open_flag)
            # open mode
            open_mode = int(line.split(',')[3], 8) # save mode as decimal
            all_open_mode.append(open_mode)
        # write_file: open flags, lseek offset, write size
        elif ops_name == 'write_file':
            # open flags
            open_flag = int(line.split(',')[2])
            all_open_flags.append(open_flag)
            # lseek offset
            lseek_offset = int(line.split(',')[4])
            all_lseek_offset.append(lseek_offset)
            # write size
            write_size = int(line.split(',')[5])
            all_write_count.append(write_size)
        # truncate: truncate length
        elif ops_name == 'truncate':
            # truncate length
            truncate_length = int(line.split(',')[2])
            all_truncate_length.append(truncate_length)
        # mkdir: mkdir mode
        elif ops_name == 'mkdir':
            # mkdir mode
            mkdir_mode = int(line.split(',')[2], 8) # save mode as decimal
            all_mkdir_mode.append(mkdir_mode)
        # chmod: chmod mode
        elif ops_name == 'chmod':
            # chmod mode
            chmod_mode = int(line.split(',')[2], 8) # save mode as decimal
            all_chmod_mode.append(chmod_mode)
        # setxattr: setxattr size, setxattr flags
        elif ops_name == 'setxattr':
            # setxattr size
            setxattr_size = int(line.split(',')[4])
            all_setxattr_size.append(setxattr_size)
            # setxattr flags
            setxattr_flag = int(line.split(',')[5])
            all_setxattr_flags.append(setxattr_flag)
        # Other operations: unlink, rmdir, chown_file, chgrp_file, removexattr, rename, link, symlink
        else:
            continue

all_input_cov['open']['flags'] = interpret_open_flags(all_open_flags)
all_input_cov['open']['mode'] = list_to_count_dict(all_open_mode)
all_input_cov['write']['count'] = list_to_count_dict(all_write_count)
all_input_cov['lseek']['offset'] = list_to_count_dict(all_lseek_offset)
all_input_cov['truncate']['length'] = list_to_count_dict(all_truncate_length)
all_input_cov['mkdir']['mode'] = list_to_count_dict(all_mkdir_mode)
all_input_cov['chmod']['mode'] = list_to_count_dict(all_chmod_mode)
all_input_cov['setxattr']['size'] = list_to_count_dict(all_setxattr_size)
all_input_cov['setxattr']['flags'] = list_to_setxattr_flags_dict(all_setxattr_flags)

# Dump the "all_input_cov" to both json file and pickle file
with open('input_cov_mcfs_{}.pkl'.format(name_suffix), 'wb') as f:
    pickle.dump(all_input_cov, f)

with open('input_cov_mcfs_{}.json'.format(name_suffix), 'w') as fout:
    input_cov_str = json.dumps(all_input_cov, indent=4)
    print(input_cov_str, file=fout)

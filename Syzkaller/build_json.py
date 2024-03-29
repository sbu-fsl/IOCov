#!/usr/bin/env python3

#
# Copyright (c) 2020-2024 Yifei Liu
# Copyright (c) 2020-2024 Rohan Bansal
# Copyright (c) 2020-2024 Erez Zadok
# Copyright (c) 2020-2024 Stony Brook University
# Copyright (c) 2020-2024 The Research Foundation of SUNY
#
# You can redistribute it and/or modify it under the terms of the Apache License, 
# Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).
#

import pandas as pd
import json
import pickle
import sys
# Make sure you are in Syzkaller folder
sys.path.append('../src')
from constants import *
from utilities import *

# name_suffix uses underscore "_"
name_suffix = '40mins_2023_0809_0037'

# xlsx_file uses hyphen "-"
xlsx_file = 'raw-syzkaller-syscalls-40mins-2023-0809-0037.xlsx'

# Fetch each syscall sheet as a data frame 

# open and its variants
# TODO: openat2 does not have flags or mode argument 
df_open = pd.read_excel(xlsx_file, sheet_name='open')
df_openat = pd.read_excel(xlsx_file, sheet_name='openat')
df_creat = pd.read_excel(xlsx_file, sheet_name='creat')
# df_openat2 = pd.read_excel(xlsx_file, sheet_name='openat2')

# read and its variants 
df_read = pd.read_excel(xlsx_file, sheet_name='read')
df_pread64 = pd.read_excel(xlsx_file, sheet_name='pread64')

# write and its variants 
df_write = pd.read_excel(xlsx_file, sheet_name='write')
df_pwrite64 = pd.read_excel(xlsx_file, sheet_name='pwrite64')

# TODO: llseek not captured by Syzkaller config
# lseek and its variants 
df_lseek = pd.read_excel(xlsx_file, sheet_name='lseek')
# df_llseek = pd.read_excel(xlsx_file, sheet_name='llseek')

# truncate and its variants
df_truncate = pd.read_excel(xlsx_file, sheet_name='truncate')
df_ftruncate = pd.read_excel(xlsx_file, sheet_name='ftruncate')

# mkdir and its variants
df_mkdir = pd.read_excel(xlsx_file, sheet_name='mkdir')
df_mkdirat = pd.read_excel(xlsx_file, sheet_name='mkdirat')

# chmod and its variants
df_chmod = pd.read_excel(xlsx_file, sheet_name='chmod')
df_fchmod = pd.read_excel(xlsx_file, sheet_name='fchmod')
df_fchmodat = pd.read_excel(xlsx_file, sheet_name='fchmodat')

# NO NEED TO HANDLE close and its variants, chdir and its variants
# df_close = pd.read_excel(xlsx_file, sheet_name='close')
# df_close_range = pd.read_excel(xlsx_file, sheet_name='close_range')

# setxattr and its variants
df_setxattr = pd.read_excel(xlsx_file, sheet_name='setxattr')
df_lsetxattr = pd.read_excel(xlsx_file, sheet_name='lsetxattr')
df_fsetxattr = pd.read_excel(xlsx_file, sheet_name='fsetxattr')

# getxattr and its variants
df_getxattr = pd.read_excel(xlsx_file, sheet_name='getxattr')
df_lgetxattr = pd.read_excel(xlsx_file, sheet_name='lgetxattr')
df_fgetxattr = pd.read_excel(xlsx_file, sheet_name='fgetxattr')

# key: base-syscall
# value: a dict 
### key: each argument name of the base-syscall and its variants
### value: a dict
##### key: each input partition 
##### value: frequency of each input partition
all_input_cov = init_input_cov()

# print('all_input_cov: ', all_input_cov)

# Handle open: extract inputs from all syscall variants and concatenate them into one

### Handle open flags 
open_flags = df_open['flags'].tolist()
openat_flags = df_openat['flags'].tolist()

all_open_flags_hex = open_flags + openat_flags

all_open_flags = [int(hex_str.strip(), 16) for hex_str in all_open_flags_hex]
##### Handle open flags for creat() specifically 
all_open_flags += [CREAT_FLAG_DEC] * len(df_creat)
all_input_cov['open']['flags'] = interpret_open_flags(all_open_flags)

### Handle open mode
# Remove empty open mode entries due to different argument numbers for open and openat
df_open = df_open.dropna(subset=['mode'])
df_openat = df_openat.dropna(subset=['mode'])

open_mode = df_open['mode'].tolist()
openat_mode = df_openat['mode'].tolist()
creat_mode = df_creat['mode'].tolist()

all_open_mode_hex = open_mode + openat_mode + creat_mode

all_open_mode = [int(hex_str.strip(), 16) for hex_str in all_open_mode_hex]

all_input_cov['open']['mode'] = list_to_count_dict(all_open_mode)

# Handle read

### Handle read count
read_count = df_read['count'].tolist()
pread64_count = df_pread64['count'].tolist()

all_read_count_hex = read_count + pread64_count

all_read_count = [int(hex_str.strip(), 16) for hex_str in all_read_count_hex]

all_input_cov['read']['count'] = list_to_count_dict(all_read_count)

### Handle read offset
all_read_offset_hex = df_pread64['offset'].tolist()

all_read_offset = [int(hex_str.strip(), 16) for hex_str in all_read_offset_hex]

all_input_cov['read']['offset'] = list_to_count_dict(all_read_offset)

# Handle write

### Handle write count
write_count = df_write['count'].tolist()
pwrite64_count = df_pwrite64['count'].tolist()

all_write_count_hex = write_count + pwrite64_count

all_write_count = [int(hex_str.strip(), 16) for hex_str in all_write_count_hex]

all_input_cov['write']['count'] = list_to_count_dict(all_write_count)

### Handle write offset
all_write_offset_hex = df_pwrite64['offset'].tolist()

all_write_offset = [int(hex_str.strip(), 16) for hex_str in all_write_offset_hex]

all_input_cov['write']['offset'] = list_to_count_dict(all_write_offset)

# Handle lseek

### Handle lseek offset
all_lseek_offset_hex = df_lseek['offset'].tolist()

all_lseek_offset = [int(hex_str.strip(), 16) for hex_str in all_lseek_offset_hex]

all_input_cov['lseek']['offset'] = list_to_count_dict(all_lseek_offset)

### Handle lseek whence
all_lseek_whence_hex = df_lseek['whence'].tolist()

all_lseek_whence = [int(hex_str.strip(), 16) for hex_str in all_lseek_whence_hex]

all_input_cov['lseek']['whence'] = list_to_whence_dict(all_lseek_whence)

# Handle truncate

### Handle truncate length
truncate_length = df_truncate['length'].tolist()
ftruncate_length = df_ftruncate['length'].tolist()

all_truncate_length_hex = truncate_length + ftruncate_length

all_truncate_length = [int(hex_str.strip(), 16) for hex_str in all_truncate_length_hex]

all_input_cov['truncate']['length'] = list_to_count_dict(all_truncate_length)

# Handle mkdir

### Handle mkdir mode
mkdir_mode = df_mkdir['mode'].tolist()
mkdirat_mode = df_mkdirat['mode'].tolist()

all_mkdir_mode_hex = mkdir_mode + mkdirat_mode

all_mkdir_mode = [int(hex_str.strip(), 16) for hex_str in all_mkdir_mode_hex]

all_input_cov['mkdir']['mode'] = list_to_count_dict(all_mkdir_mode)

# Handle chmod

### Handle chmod mode

chmod_mode = df_chmod['mode'].tolist()
fchmod_mode = df_fchmod['mode'].tolist()
fchmodat_mode = df_fchmodat['mode'].tolist()

all_chmod_mode_hex = chmod_mode + fchmod_mode + fchmodat_mode

all_chmod_mode = [int(hex_str.strip(), 16) for hex_str in all_chmod_mode_hex]

all_input_cov['chmod']['mode'] = list_to_count_dict(all_chmod_mode)

# Handle setxattr

### Handle setxattr mode

setxattr_size = df_setxattr['size'].tolist()
lsetxattr_size = df_lsetxattr['size'].tolist()
fsetxattr_size = df_fsetxattr['size'].tolist()

all_setxattr_size_hex = setxattr_size + lsetxattr_size + fsetxattr_size

all_setxattr_size = [int(hex_str.strip(), 16) for hex_str in all_setxattr_size_hex]

all_input_cov['setxattr']['size'] = list_to_count_dict(all_setxattr_size)

### Handle setxattr flags

setxattr_flags = df_setxattr['flags'].tolist()
lsetxattr_flags = df_lsetxattr['flags'].tolist()
fsetxattr_flags = df_fsetxattr['flags'].tolist()

all_setxattr_flags_hex = setxattr_flags + lsetxattr_flags + fsetxattr_flags

all_setxattr_flags = [int(hex_str.strip(), 16) for hex_str in all_setxattr_flags_hex]

all_input_cov['setxattr']['flags'] = list_to_setxattr_flags_dict(all_setxattr_flags)

# Handle getxattr

getxattr_size = df_getxattr['size'].tolist()
lgetxattr_size = df_lgetxattr['size'].tolist()
fgetxattr_size = df_fgetxattr['size'].tolist()

all_getxattr_size_hex = getxattr_size + lgetxattr_size + fgetxattr_size

all_getxattr_size = [int(hex_str.strip(), 16) for hex_str in all_getxattr_size_hex]

all_input_cov['getxattr']['size'] = list_to_count_dict(all_getxattr_size)

# Dump the "all_input_cov" to both json file and pickle file
with open('input_cov_syzkaller_{}.pkl'.format(name_suffix), 'wb') as f:
    pickle.dump(all_input_cov, f)

with open('input_cov_syzkaller_{}.json'.format(name_suffix), 'w') as fout:
    input_cov_str = json.dumps(all_input_cov, indent=4)
    print(input_cov_str, file=fout)

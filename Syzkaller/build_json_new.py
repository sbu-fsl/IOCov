#!/usr/bin/env python3

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
# xlsx_file = 'raw-syzkaller-syscalls-40mins-2023-0809-0037.xlsx'
xlsx_file = '/mnt/c/Users/Rohan/syzkaller/IOCov/Syzkaller/raw-syzkaller-syscalls-syzkaller.xlsx'
# Fetch each syscall sheet as a data frame 

# open and its variants
# TODO: openat2 does not have flags or mode argument 
df_open = pd.read_excel(xlsx_file, sheet_name='open')
print("df_open")

# read and its variants 
df_read = pd.read_excel(xlsx_file, sheet_name='read')
print("df_read")

# write and its variants 
df_write = pd.read_excel(xlsx_file, sheet_name='write')
print("df_write")

# lseek and its variants 
df_lseek = pd.read_excel(xlsx_file, sheet_name='lseek')
print("df_lseek")

# truncate and its variants
df_truncate = pd.read_excel(xlsx_file, sheet_name='truncate')
print("df_truncate")

# mkdir and its variants
df_mkdir = pd.read_excel(xlsx_file, sheet_name='mkdir')
print("df_mkdir")

# chmod and its variants
df_chmod = pd.read_excel(xlsx_file, sheet_name='chmod')
print("df_chmod")

# setxattr and its variants
df_setxattr = pd.read_excel(xlsx_file, sheet_name='setxattr')
print("df_setxattr")

df_removexattr = pd.read_excel(xlsx_file, sheet_name='removexattr')
print("df_removexattr")
df_link = pd.read_excel(xlsx_file, sheet_name='link')
print("df_link")
df_unlink = pd.read_excel(xlsx_file, sheet_name='unlink')
print("df_unlink")
df_symlink = pd.read_excel(xlsx_file, sheet_name='symlink')
print("df_symlink")
df_rmdir = pd.read_excel(xlsx_file, sheet_name='rmdir')
print("df_rmdir")
df_rename = pd.read_excel(xlsx_file, sheet_name='rename')
print("df_rename")
df_statfs = pd.read_excel(xlsx_file, sheet_name='statfs')
print("df_statfs")


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

all_open_flags_hex = open_flags

all_open_flags = [int(hex_str.strip(), 16) for hex_str in all_open_flags_hex if ('x' in hex_str and '#' not in hex_str)]
##### Handle open flags for creat() specifically 
#all_open_flags += [CREAT_FLAG_DEC] * len(df_creat)
all_input_cov['open']['flags'] = interpret_open_flags(all_open_flags)

### Handle open mode
# Remove empty open mode entries due to different argument numbers for open and openat
df_open = df_open.dropna(subset=['mode'])

open_mode = df_open['mode'].tolist()

all_open_mode_hex = open_mode

all_open_mode = [int(hex_str.strip(), 16) for hex_str in all_open_mode_hex if ('x' in hex_str and '#' not in hex_str)]

all_input_cov['open']['mode'] = list_to_count_dict(all_open_mode)

print("open handled")
# Handle read

### Handle read count
read_count = df_read['count'].tolist()

all_read_count_hex = read_count

all_read_count = [int(hex_str.strip(), 16) for hex_str in all_read_count_hex if (hex_str.count('x')==1 and '#' not in hex_str)]

all_input_cov['read']['count'] = list_to_count_dict(all_read_count)
print("read handled")

# Handle write

### Handle write count
write_count = df_write['count'].tolist()

all_write_count_hex = write_count

all_write_count = [int(hex_str.strip(), 16) for hex_str in all_write_count_hex if ('x' in hex_str and '#' not in hex_str)]

all_input_cov['write']['count'] = list_to_count_dict(all_write_count)

print("write handled")

# Handle lseek

### Handle lseek offset
all_lseek_offset_hex = df_lseek['offset'].tolist()

all_lseek_offset = [int(hex_str.strip(), 16) for hex_str in all_lseek_offset_hex if ('x' in hex_str and '#' not in hex_str)]

all_input_cov['lseek']['offset'] = list_to_count_dict(all_lseek_offset)

### Handle lseek whence
all_lseek_whence_hex = df_lseek['whence'].tolist()

all_lseek_whence = [int(hex_str.strip(), 16) for hex_str in all_lseek_whence_hex if ('x' in hex_str and '#' not in hex_str)]

all_input_cov['lseek']['whence'] = list_to_whence_dict(all_lseek_whence)
print("lseek handled")

# Handle truncate

### Handle truncate length
truncate_length = df_truncate['length'].tolist()

all_truncate_length_hex = truncate_length

all_truncate_length = [int(hex_str.strip(), 16) for hex_str in all_truncate_length_hex if ('x' in hex_str and '#' not in hex_str)]

all_input_cov['truncate']['length'] = list_to_count_dict(all_truncate_length)
print("truncate handled")

# Handle mkdir

### Handle mkdir mode
mkdir_mode = df_mkdir['mode'].tolist()

all_mkdir_mode_hex = mkdir_mode

all_mkdir_mode = [int(hex_str.strip(), 16) for hex_str in all_mkdir_mode_hex if ('x' in hex_str and '#' not in hex_str)]

all_input_cov['mkdir']['mode'] = list_to_count_dict(all_mkdir_mode)
print("mkdir handled")

# Handle chmod

### Handle chmod mode

chmod_mode = df_chmod['mode'].tolist()

all_chmod_mode_hex = chmod_mode

all_chmod_mode = [int(hex_str.strip(), 16) for hex_str in all_chmod_mode_hex if ('x' in hex_str and '#' not in hex_str)]

all_input_cov['chmod']['mode'] = list_to_count_dict(all_chmod_mode)
print("chmod handled")

# Handle setxattr

### Handle setxattr mode

setxattr_size = df_setxattr['size'].tolist()

all_setxattr_size_hex = setxattr_size

all_setxattr_size = [int(hex_str.strip(), 16) for hex_str in all_setxattr_size_hex if ('x' in hex_str and '#' not in hex_str)]

all_input_cov['setxattr']['size'] = list_to_count_dict(all_setxattr_size)

### Handle setxattr flags

setxattr_flags = df_setxattr['flags'].tolist()

all_setxattr_flags_hex = setxattr_flags

all_setxattr_flags = [int(hex_str.strip(), 16) for hex_str in all_setxattr_flags_hex if ('x' in hex_str and '#' not in hex_str)]

all_input_cov['setxattr']['flags'] = list_to_setxattr_flags_dict(all_setxattr_flags)
print("setxattr handled")

# handle removexattr

all_removexattr_path_hex = df_removexattr['path'].tolist()
all_removexattr_name_hex = df_removexattr['name'].tolist()

all_removexattr_path = [int(hex_str.strip(), 16) for hex_str in all_removexattr_path_hex if ('x' in hex_str and '#' not in hex_str)]
all_removexattr_name = [int(hex_str.strip(), 16) for hex_str in all_removexattr_name_hex if ('x' in hex_str and '#' not in hex_str)]

all_input_cov['removexattr']['path'] = list_to_count_dict(all_removexattr_path)
all_input_cov['removexattr']['name'] = list_to_count_dict(all_removexattr_name)
print("removexattr handled")

# handle link

all_link_oldpath_hex = df_link['oldpath'].tolist()
all_link_newpath_hex = df_link['newpath'].tolist()

all_link_oldpath = [int(hex_str.strip(), 16) for hex_str in all_link_oldpath_hex if ('x' in hex_str and '#' not in hex_str)]
all_link_newpath = [int(hex_str.strip(), 16) for hex_str in all_link_newpath_hex if ('x' in hex_str and '#' not in hex_str)]

all_input_cov['link']['oldpath'] = list_to_count_dict(all_link_oldpath)
all_input_cov['link']['newpath'] = list_to_count_dict(all_link_newpath)
print("link handled")

# handle unlink
'''
all_unlink_pathname_hex = df_unlink['pathname'].tolist()

all_unlink_pathname = [int(hex_str.strip(), 16) for hex_str in all_unlink_pathname_hex if (hex_str != '' and 'x' in hex_str and '#' not in hex_str)]

all_input_cov['unlink']['pathname'] = list_to_count_dict(all_unlink_pathname)
print("unlink handled")
'''
#handle symlink

all_symlink_target_hex = df_symlink['target'].tolist()
all_symlink_linkpath_hex = df_symlink['linkpath'].tolist()

all_symlink_target = [int(hex_str.strip(), 16) for hex_str in all_symlink_target_hex if ('x' in hex_str and '#' not in hex_str)]
all_symlink_linkpath = [int(hex_str.strip(), 16) for hex_str in all_symlink_linkpath_hex if ('x' in hex_str and '#' not in hex_str)]

all_input_cov['symlink']['target'] = list_to_count_dict(all_symlink_target)
all_input_cov['symlink']['linkpath'] = list_to_count_dict(all_symlink_linkpath)
print("symlink handled")

# handle rmdir

all_rmdir_pathname_hex = df_rmdir['pathname'].tolist()

all_rmdir_pathname = [int(hex_str.strip(), 16) for hex_str in all_rmdir_pathname_hex if ('x' in hex_str and '#' not in hex_str and '(' not in hex_str)]

all_input_cov['rmdir']['pathname'] = list_to_count_dict(all_rmdir_pathname)
print("rmdir handled")

# handle rename

all_rename_oldpath_hex = df_rename['oldpath'].tolist()
all_rename_newpath_hex = df_rename['newpath'].tolist()

all_rename_oldpath = [int(hex_str.strip(), 16) for hex_str in all_rename_oldpath_hex if ('x' in hex_str and '#' not in hex_str)]
all_rename_newpath = [int(hex_str.strip(), 16) for hex_str in all_rename_newpath_hex if ('x' in hex_str and '#' not in hex_str)]

all_input_cov['rename']['oldpath'] = list_to_count_dict(all_rename_oldpath)
all_input_cov['rename']['newpath'] = list_to_count_dict(all_rename_newpath)
print("rename handled")

# handle statfs

all_statfs_path_hex = df_statfs['path'].tolist()
all_statfs_buf_hex = df_statfs['buf'].tolist()

all_statfs_path = [int(hex_str.strip(), 16) for hex_str in all_statfs_path_hex if ('x' in hex_str and '#' not in hex_str)]
all_statfs_buf = [int(hex_str.strip(), 16) for hex_str in all_statfs_buf_hex if ('x' in hex_str and '#' not in hex_str)] 

all_input_cov['statfs']['path'] = list_to_count_dict(all_statfs_path)
all_input_cov['statfs']['buf'] = list_to_count_dict(all_statfs_buf)
print("statfs handled")

# Dump the "all_input_cov" to both json file and pickle file
with open('input_cov_syzkaller_{}.pkl'.format(name_suffix), 'wb') as f:
    pickle.dump(all_input_cov, f)

with open('input_cov_syzkaller_{}.json'.format(name_suffix), 'w') as fout:
    input_cov_str = json.dumps(all_input_cov, indent=4)
    print(input_cov_str, file=fout)

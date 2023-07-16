#!/usr/bin/env python3

import pandas as pd
import json
import sys
# Make sure you are in Syzkaller folder
sys.path.append('../src')
from constants import *
from utilities import *

xlsx_file = 'raw-syzkaller-syscalls.xlsx'

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




### Handle open mode


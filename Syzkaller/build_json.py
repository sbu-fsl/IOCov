#!/usr/bin/env python3

import pandas as pd
import json
import sys
# Make sure you are in Syzkaller folder
sys.path.append('../src')
from constants import *

xlsx_file = 'raw-syzkaller-syscalls.xlsx'

# Fetch each syscall sheet as a data frame 

# open and its variants
df_open = pd.read_excel(xlsx_file, sheet_name='open')
df_openat = pd.read_excel(xlsx_file, sheet_name='openat')
df_creat = pd.read_excel(xlsx_file, sheet_name='creat')
df_openat2 = pd.read_excel(xlsx_file, sheet_name='openat2')

# read and its variants 
df_read = pd.read_excel(xlsx_file, sheet_name='read')
df_pread64 = pd.read_excel(xlsx_file, sheet_name='pread64')

# write and its variants 
df_write = pd.read_excel(xlsx_file, sheet_name='write')
df_pwrite64 = pd.read_excel(xlsx_file, sheet_name='pwrite64')

# TODO: llseek not captured by Syzkaller config
# lseek and its variants 
df_lseek = pd.read_excel(xlsx_file, sheet_name='lseek')
df_llseek = pd.read_excel(xlsx_file, sheet_name='llseek')

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

# hex_str = "F"
# binary_str = int(hex_str, 16)
# print(binary_str)

# print('df_open: \n', df_open)
# print('--------------------------------')
# print('df_openat: \n', df_openat)
# print('--------------------------------')
# print('df_creat: \n', df_creat)
# print('--------------------------------')
# print('df_openat2: \n', df_openat2)
# print('--------------------------------')
# sys.exit()

## handle open

open_flag_binary = []
open_mode_int = []

for index, row in df_openat.iterrows():
    if('0x' not in row['flags_hex']):
        open_flag_binary.append(int(row['flags_hex'], 16))
        open_mode_int.append(int(row['mode_hex'], 16))
    else:
        open_flag_binary.append(0)
        open_mode_int.append(int(row['mode_hex'], 16))

df_openat['flags_binary'] = open_flag_binary
df_openat['mode_int'] = open_mode_int

dict_open_flags = {}
dict_open_mode = {}

for flag in OPEN_BIT_FLAGS.keys():
    dict_open_flags[OPEN_BIT_FLAGS[flag]] = 0

for flag_binary in open_flag_binary:
    for flag in OPEN_BIT_FLAGS.keys():
        flag2 = int(str(flag), 16)
        if flag_binary & flag2 == flag2:
            if OPEN_BIT_FLAGS[flag] in dict_open_flags:
                dict_open_flags[OPEN_BIT_FLAGS[flag]] += 1

for mode in open_mode_int:
    if mode in dict_open_mode:
        dict_open_mode[mode] += 1
    else:
        dict_open_mode[mode] = 1

dict_open = {"flags" : dict_open_flags, "mode" : dict_open_mode}

## handle creat

creat_mode_int = []

for index, row in df_creat.iterrows():
    if str(row['mode_hex']) != 'nan' and ('=' not in str(row['mode_hex'])) and ('?' not in str(row['mode_hex'])):
        creat_mode_int.append(int(str(row['mode_hex']), 16))
    else:
        creat_mode_int.append(0)

df_creat['mode_int'] = creat_mode_int

dict_creat_mode = {}

for mode in open_mode_int:
    if mode in dict_creat_mode:
        dict_creat_mode[mode] += 1
    else:
        dict_creat_mode[mode] = 1

dict_creat = {"mode" : dict_creat_mode}

## handle read

read_count_int = []

for index, row in df_read.iterrows():
    if str(row['count_hex']) != 'nan' and ('x' not in str(row['count_hex'])) and (')' not in row['count_hex']):
        read_count_int.append(int(row['count_hex'], 16))
    else:
        read_count_int.append(0)

df_read['count_int'] = read_count_int

dict_read_count = {}

for count in read_count_int:
    if count in dict_read_count:
        dict_read_count[count] += 1
    else:
        dict_read_count[count] = 1

dict_read = {"count" : dict_read_count}

## handle pread64

pread64_count_int = []
pread64_offset_int = []

for index, row in df_pread64.iterrows():
    pread64_offset_int.append(int(str(row['offset_hex']), 16))
    pread64_count_int.append(int(str(row['count_hex']), 16))

df_pread64['count_int'] = pread64_count_int
df_pread64['offset_int'] = pread64_offset_int

dict_pread64_count = {}
dict_pread64_offset = {}

for count in pread64_count_int:
    if count in dict_pread64_count:
        dict_pread64_count[count] += 1
    else:
        dict_pread64_count[count] = 1

for offset in pread64_offset_int:
    if offset in dict_pread64_offset:
        dict_pread64_offset[offset] += 1
    else:
        dict_pread64_offset[offset] = 1

dict_pread64 = {"count" : dict_pread64_count, "offset" : dict_pread64_offset}
 
## handle write

write_count_int = []

for index, row in df_write.iterrows():
    if ('n' not in str(row['count_hex'])) and ('/' not in str(row['count_hex'])) and ("'" not in str(row['count_hex'])) and ('=' not in str(row['count_hex'])) and ('"' not in str(row['count_hex'])) and ('N' not in str(row['count_hex'])):
        write_count_int.append(int(row['count_hex'], 16))
    else:
       write_count_int.append(0)

df_write['count_int'] = write_count_int

dict_write_count = {}

for count in write_count_int:
    if count in dict_write_count:
        dict_write_count[count] += 1
    else:
        dict_write_count[count] = 1

dict_write = {"count" : dict_write_count}

## handle pwrite64

pwrite64_count_int = []
pwrite64_offset_int = []

for index, row in df_pwrite64.iterrows():
    pwrite64_offset_int.append(int(str(row['offset_hex']), 16))
    pwrite64_count_int.append(int(str(row['count_hex']), 16))

df_pwrite64['count_int'] = pwrite64_count_int
df_pwrite64['offset_int'] = pwrite64_offset_int

dict_pwrite64_count = {}
dict_pwrite64_offset = {}

for count in pwrite64_count_int:
    if count in dict_pwrite64_count:
        dict_pwrite64_count[count] += 1
    else:
        dict_pwrite64_count[count] = 1

for offset in pwrite64_offset_int:
    if offset in dict_pwrite64_offset:
        dict_pwrite64_offset[offset] += 1
    else:
        dict_pwrite64_offset[offset] = 1

dict_pwrite64 = {"count" : dict_pwrite64_count, "offset" : dict_pwrite64_offset}

## handle lseek

lseek_whence_int = []
lseek_offset_int = []

for index, row in df_lseek.iterrows():
    lseek_offset_int.append(int(str(row['offset_hex']), 16))
    lseek_whence_int.append(int(str(row['whence_hex']), 16))

df_lseek['whence_int'] = lseek_whence_int
df_lseek['offset_int'] = lseek_offset_int

dict_lseek_whence = {}
dict_lseek_offset = {}

for whence in LSEEK_WHENCE_NUMS.keys():
    dict_lseek_whence[LSEEK_WHENCE_NUMS[whence]] = 0

for whence in lseek_whence_int:
    if whence in LSEEK_WHENCE_NUMS:
        dict_lseek_whence[LSEEK_WHENCE_NUMS[whence]] += 1

for offset in lseek_offset_int:
    if offset in dict_lseek_offset:
        dict_lseek_offset[offset] += 1
    else:
        dict_lseek_offset[offset] = 1

dict_lseek = {"whence" : dict_lseek_whence, "offset" : dict_lseek_offset}

## handle truncate

truncate_length_int = []

for index, row in df_truncate.iterrows():
    truncate_length_int.append(int(row['length_hex'], 16))

df_truncate['length_int'] = truncate_length_int

dict_truncate_length = {}

for length in truncate_length_int:
    if length in dict_truncate_length:
        dict_truncate_length[length] += 1
    else:
        dict_truncate_length[length] = 1

dict_truncate = {"length" : dict_truncate_length}

## handle mkdir

mkdir_mode_int = []

for index, row in df_mkdir.iterrows():
    mkdir_mode_int.append(int(row['mode_hex'], 16))

df_mkdir['mode_int'] = mkdir_mode_int

dict_mkdir_mode = {}

for mode in mkdir_mode_int:
    if mode in dict_mkdir_mode:
        dict_mkdir_mode[mode] += 1
    else:
        dict_mkdir_mode[mode] = 1

dict_mkdir = {"mode" : dict_mkdir_mode}

## handle chmod

chmod_mode_int = []

for index, row in df_chmod.iterrows():
    chmod_mode_int.append(int(row['mode_hex'], 16))

df_chmod['mode_int'] = chmod_mode_int

dict_chmod_mode = {}

for mode in chmod_mode_int:
    if mode in dict_chmod_mode:
        dict_chmod_mode[mode] += 1
    else:
        dict_chmod_mode[mode] = 1

dict_chmod = {"mode" : dict_chmod_mode}

## handle close

close_flags_int = []

for index, row in df_close.iterrows():
    close_flags_int.append(int(str(row['flags_hex']), 16))

df_close['flags_int'] = close_flags_int

dict_close_flags = {}

for flag in close_flags_int:
    if flag in dict_close_flags:
        dict_close_flags[flag] += 1
    else:
        dict_close_flags[flag] = 1

dict_close = {"flags" : dict_close_flags}

## handle setxattr

setxattr_size_int = []
setxattr_flags_int = []

for index, row in df_setxattr.iterrows():
    if ('}' not in str(row['flags_hex'])):
        setxattr_flags_int.append(int(str(row['flags_hex']), 16))
    else:
        setxattr_flags_int.append(0)
    if ('}' not in str(row['size_hex'])):
        setxattr_size_int.append(int(str(row['size_hex']), 16))
    else:
        setxattr_size_int.append(0)

df_setxattr['size_int'] = setxattr_size_int
df_setxattr['flags_int'] = setxattr_flags_int

dict_setxattr_flags = {}
dict_setxattr_size = {}

for flag in SETXATTR_FLAGS_NUMS.keys():
    dict_setxattr_flags[SETXATTR_FLAGS_NUMS[flag]] = 0

for flag in setxattr_flags_int:
    if flag in SETXATTR_FLAGS_NUMS:
        dict_setxattr_flags[SETXATTR_FLAGS_NUMS[flag]] += 1

for size in setxattr_size_int:
    if size in dict_setxattr_size:
        dict_setxattr_size[size] += 1
    else:
        dict_setxattr_size[size] = 1

dict_setxattr = {"size" : dict_setxattr_size, "flags" : dict_setxattr_flags}

## handle getxattr

getxattr_size_int = []

for index, row in df_getxattr.iterrows():
    getxattr_size_int.append(int(str(row['size_hex']), 16))

df_getxattr['size_int'] = getxattr_size_int

dict_getxattr_size = {}

for size in getxattr_size_int:
    if size in dict_getxattr_size:
        dict_getxattr_size[size] += 1
    else:
        dict_getxattr_size[size] = 1

dict_getxattr = {"size" : dict_getxattr_size}



dict = {"open" : dict_open, "creat" : dict_creat, "read" : dict_read, "pread64"
        : dict_pread64, "write" : dict_write, "pwrite64" : dict_pwrite64, 
        "lseek" : dict_lseek, "truncate" : dict_truncate, "mkdir" : dict_mkdir
        , "chmod" : dict_chmod, "close" : dict_close, "setxattr" : dict_setxattr
        , "getxattr" : dict_getxattr}

json_object = json.dumps(dict, indent = 4) 
print(json_object)

print(json_object)

with open("syzkaller_cov.json", "w") as outfile:
    outfile.write(json_object)







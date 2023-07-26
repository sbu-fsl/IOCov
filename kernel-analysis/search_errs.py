#!/usr/bin/env python3

import os
import fnmatch
import errno
import pickle
import csv
import sys

need_search = True
need_post_testing = False
print_all = False

# Combine the kernel occurrences with file system testing into a csv file
post_header = ['Xfstests', 
                'Crashmonkey']

# Output pkl files for each file system testing
post_pkl_files = ['output_cov_all_xfstests_xattrs.pkl', 
                    'output_cov_crashmonkey.pkl']

# sgdp02
# linux_dir = '/mcfs/Linux_Kernel_Install/linux-stable/fs/ext4'
# linux_dir = '/mcfs/Linux_Kernel_Install/linux-stable'

# yifeilatest1
linux_dir = '/mcfs/Linux_Kernel_Install/linux-6.3'

# Kernel directories to search
linux_dirs = [linux_dir, 
                linux_dir + '/fs/ext4', 
                linux_dir + '/fs/xfs', 
                linux_dir + '/fs/btrfs',
                linux_dir + '/fs']

# csv header 
labels = ['All-Linux-src',
            'Ext4-src',
            'XFS-src',
            'BtrFS-src',
            'All-FS-src']

percent_suffix = '-percent'
percent_labels = [ label + percent_suffix for label in labels ]

# Search for C source files
pattern = '*.c'

# List of all the error codes in string
err_list = []
# Dict -- Key: error number in integer, Value: error code in string
errno_err_dict = {}
for name in dir(errno): 
    if name.startswith('E'):
        err_list.append(name)
        errno_err_dict[getattr(errno, name)] = name

# print('err_list: ', err_list)
# print('len(err_list): ', len(err_list))

# If we need to search the kernel sources and obtain pkl files 
# One label for each pkl file
# If we don't need to search, we should already have these pkl files
if need_search:
    for i in range(len(linux_dirs)):
        linux_dir = linux_dirs[i]
        err_cnt = {}
        for name in err_list: 
            err_cnt[name] = 0
        # Use os.walk to recursively search for files in the linux_dir
        for root, dirnames, filenames in os.walk(linux_dir):
            for fn in fnmatch.filter(filenames, pattern):
                # Print the absolute path of each C source file found
                abs_fn = os.path.abspath(os.path.join(root, fn))
                # print(abs_fn)
                with open(abs_fn, 'r') as f:
                    contents = f.read()
                    for err in err_list:
                        count = contents.count(err)
                        err_cnt[err] += count
        if print_all:
            print(labels[i] + ': ')
            print(err_cnt)
            print('===============')
        with open('{}_err_count.pkl'.format(labels[i]), 'wb') as f:
            pickle.dump(err_cnt, f)

# Read kernel search pkl files 
# all_err_cnt: key: each label (csv header); value: dict of error code count
#       key: error code; value: count
all_err_cnt = {}
for i in range(len(labels)):
    with open('{}_err_count.pkl'.format(labels[i]), 'rb') as f:
        err_cnt = pickle.load(f)
        all_err_cnt[labels[i]] = err_cnt

all_post_err_cnt = {}
if need_post_testing:
    for i in range(len(post_header)):
        post_err_cnt = {}
        for name in err_list: 
            post_err_cnt[name] = 0
        with open(post_pkl_files[i], 'rb') as f:
            output_cov = pickle.load(f)
            for sc, outputs in output_cov.items():
                for ret, cnt in outputs.items():
                    if ret < 0 and abs(ret) in errno_err_dict.keys():
                        post_err_cnt[errno_err_dict[abs(ret)]] += cnt

        all_post_err_cnt[post_header[i]] = post_err_cnt

    # Append error code count from file system testing
    all_err_cnt.update(all_post_err_cnt)

    # Append error code header from file system testing
    labels += post_header

# print('all_err_cnt: \n', all_err_cnt)

# Count total occurrences of each error code
# total_err_cnt: key: each label (csv header); value: total count across all the error codes
total_err_cnt = {}
for label in labels:
    total_cnt = 0
    for err_str in err_list:
        total_cnt += all_err_cnt[label][err_str]
    total_err_cnt[label] = total_cnt

# print('total_err_cnt: ', total_err_cnt)

# header = ['Errno', 'Error_Code'] + labels
header = ['No.', 'Errno'] + labels + percent_labels
with open('linux_errs_summary.csv', 'w') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    for err_no in sorted(errno_err_dict.keys()):
        data = []
        err_code = errno_err_dict[err_no]
        data.append(err_no)
        data.append(err_code)
        for i in range(len(labels)):
            data.append(all_err_cnt[labels[i]][err_code])
        # Calculate the percentage
        for i in range(len(labels)):
            data.append('{:.2f} %'.format(all_err_cnt[labels[i]][err_code] / total_err_cnt[labels[i]] * 100))
        # write the data
        writer.writerow(data)

print('All completed!')

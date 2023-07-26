#!/usr/bin/env python3

import os
import fnmatch
import errno
import pickle
import csv
import sys

need_search = False

# sgdp02
# linux_dir = '/mcfs/Linux_Kernel_Install/linux-stable/fs/ext4'
# linux_dir = '/mcfs/Linux_Kernel_Install/linux-stable'

linux_dirs = ['/mcfs/Linux_Kernel_Install/linux-stable', 
                '/mcfs/Linux_Kernel_Install/linux-stable/fs/ext4', 
                '/mcfs/Linux_Kernel_Install/linux-stable/fs/xfs', 
                '/mcfs/Linux_Kernel_Install/linux-stable/fs/btrfs',
                '/mcfs/Linux_Kernel_Install/linux-stable/fs']

labels = ['All-Linux-src',
            'Ext4-src',
            'XFS-src',
            'BtrFS-src',
            'FS-src']

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

        print(labels[i] + ': ')
        print(err_cnt)
        print('===============')
        with open('{}_err_count.pkl'.format(labels[i]), 'wb') as f:
            pickle.dump(err_cnt, f)

post_header = ['Xfstests', 
                'Crashmonkey']

post_pkl_files = ['output_cov_all_xfstests_xattrs.pkl', 
                    'output_cov_crashmonkey.pkl']

all_post_err_cnt = []
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

    all_post_err_cnt.append(post_err_cnt)

all_err_cnt = []
for i in range(len(labels)):
    with open('{}_err_count.pkl'.format(labels[i]), 'rb') as f:
        err_cnt = pickle.load(f)
        all_err_cnt.append(err_cnt)

all_err_cnt += all_post_err_cnt

labels += post_header
# header = ['Errno', 'Error_Code'] + labels
header = ['No.', 'Errno'] + labels
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
            data.append(all_err_cnt[i][err_code])
        # write the data
        writer.writerow(data)

print('All completed!')

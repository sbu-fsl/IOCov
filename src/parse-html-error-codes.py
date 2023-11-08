#!/usr/bin/env python3

"""
Extract error codes from HTML files of system call manuals
"""

from bs4 import BeautifulSoup
import errno
import sys
import pickle
import os

ALL_ERROR_CODES = list(errno.errorcode.values())

# ./download-syscall-htmls.sh
# python3 parse-html-error-codes.py

# Key: must correspond to output coverage keys (i.e., meta-syscall)
# Value: list of syscall names whose web manuals need to be extracted 
#        and combine the system call error codes
SYSCALLS_MANS = {'open': ['open', 'openat2'], 'read': ['read'], 'write': ['write'], 
                'lseek': ['lseek', 'llseek'], 'truncate': ['truncate'], 
                'mkdir': ['mkdir'], 'chmod': ['chmod'], 
                'close': ['close', 'close_range'] , 'chdir': ['chdir'], 
                'setxattr': ['setxattr'], 'getxattr': ['getxattr']}

errors_dict = {}

for each_sc in SYSCALLS_MANS.keys():
    errors_dict[each_sc] = set()
    errors_dict[each_sc].add('OK')

cwd = os.getcwd()

for each_sc, each_list in SYSCALLS_MANS.items():
    for sc in each_list:
        fname = os.path.join(cwd, 'Assets/Html-Files/{}.2.html'.format(sc))
        with open(fname) as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            items = soup.find_all('b')
            for each_item in items:
                each_err = each_item.string.strip()
                if each_err in ALL_ERROR_CODES:
                    errors_dict[each_sc].add(each_err)

for each_sc in errors_dict.keys():
    each_list = list(errors_dict[each_sc])
    each_list.sort()
    errors_dict[each_sc] = each_list

print('errors_dict: ', errors_dict)
with open('errors_dict.pkl', 'wb') as f:
    pickle.dump(errors_dict, f)

print('errors_dict dumped!')

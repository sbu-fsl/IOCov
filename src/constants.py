#!/usr/bin/env python3

"""
    xfstests Constants
"""
XFSTESTS_MP = ['/mnt/test', '/mnt/scratch']

"""
    Syscall Constants
"""
SYSCALLS = {
    'open': ['open', 'openat', 'creat', 'openat2'],
    'read': ['read', 'pread64'],
    'write': ['write', 'pwrite64'],
    'lseek': ['lseek', 'llseek'],
    'truncate': ['truncate', 'ftruncate'],
    'mkdir': ['mkdir', 'mkdirat'],
    'chmod': ['chmod', 'fchmod', 'fchmodat'],
    'close': ['close', 'close_range'], # No input coverage for close()
    'chdir': ['chdir', 'fchdir'], # No input coverage for chdir()
    'setxattr': ['setxattr', 'lsetxattr', 'fsetxattr'],
    'getxattr': ['getxattr', 'lgetxattr', 'fgetxattr']
}

INPUT_SYSCALLS = {
    'open': ['open', 'openat', 'creat', 'openat2'],
    'read': ['read', 'pread64'],
    'write': ['write', 'pwrite64'],
    'lseek': ['lseek', 'llseek'],
    'truncate': ['truncate', 'ftruncate'],
    'mkdir': ['mkdir', 'mkdirat'],
    'chmod': ['chmod', 'fchmod', 'fchmodat'],
    'setxattr': ['setxattr', 'lsetxattr', 'fsetxattr'],
    'getxattr': ['getxattr', 'lgetxattr', 'fgetxattr']
}

# Ignore close()/chdir[] here because we don't measure input cov for them 
SYSCALL_ARGS = {
    'open': ['flags', 'mode'],
    'read': ['count', 'offset'],
    'write': ['count', 'offset'],
    'lseek': ['offset', 'whence'],
    'truncate': ['length'],
    'mkdir': ['mode'],
    'chmod': ['mode'],
    'close': [],
    'chdir': [],
    'setxattr': ['size', 'flags'], 
    'getxattr': ['size'],
    'removexattr' : ['path', 'name'],
    'link' : ['oldpath', 'newpath'],
    'unlink' : ['pathname'],
    'symlink' : ['target' , 'linkpath'],
    'rmdir' : ['pathname'],
    'chown' : ['pathname', 'owner', 'group'],
    'rename' : ['oldpath', 'newpath'],
    'statfs' : ['path', 'buf']
}

INPUT_PREFIX='syscall_entry_'
OUTPUT_PREFIX='syscall_exit_'
ALL_SYSCALLS = list(SYSCALLS.keys())

"""
    Open Constants
"""
# open flags with bits (eliminate O_RDONLY as we handle it differently)
OPEN_BIT_FLAGS = {
    # 0o0: 'O_RDONLY',
    0o3: 'O_ACCMODE',
    0o1: 'O_WRONLY',
    0o2: 'O_RDWR',
    0o100: 'O_CREAT',
    0o200: 'O_EXCL',
    0o400: 'O_NOCTTY',
    0o1000: 'O_TRUNC',
    0o2000: 'O_APPEND',
    0o4000: 'O_NONBLOCK',
    0o10000: 'O_DSYNC',
    0o20000: 'FASYNC',
    0o40000: 'O_DIRECT',
    0o100000: 'O_LARGEFILE',
    0o200000: 'O_DIRECTORY',
    0o400000: 'O_NOFOLLOW',
    0o1000000: 'O_NOATIME',
    0o2000000: 'O_CLOEXEC',
    0o4000000: '__O_SYNC',
    0o10000000: 'O_PATH',
    0o20000000: '__O_TMPFILE'
    }

AT_FDCWD_VAL = -100

# all open flags 21 in total
ALL_OPEN_FLAGS = [
    'O_ACCMODE',
    'O_RDONLY',
    'O_WRONLY',
    'O_RDWR',
    'O_CREAT',
    'O_EXCL',
    'O_NOCTTY',
    'O_TRUNC',
    'O_APPEND',
    'O_NONBLOCK',
    'O_DSYNC',
    'FASYNC',
    'O_DIRECT',
    'O_LARGEFILE',
    'O_DIRECTORY',
    'O_NOFOLLOW',
    'O_NOATIME',
    'O_CLOEXEC',
    '__O_SYNC',
    'O_PATH',
    '__O_TMPFILE'
    ]

"""
    close Constants
"""
CLOSE_MAX_FD = 4294967295

"""
    lseek Constants
"""
LSEEK_WHENCE_NUMS = {
    0: 'SEEK_SET',
    1: 'SEEK_CUR',
    2: 'SEEK_END',
    3: 'SEEK_DATA',
    4: 'SEEK_HOLE'
}

ALL_LSEEK_WHENCES = [
    'SEEK_SET',
    'SEEK_CUR',
    'SEEK_END',
    'SEEK_DATA',
    'SEEK_HOLE'
]

"""
    setxattr Constants
"""
SETXATTR_FLAGS_NUMS = {
    0: 'XATTR_DEFAULT',
    1: 'XATTR_CREATE',
    2: 'XATTR_REPLACE'
}

ALL_SETXATTR_FLAGS = ['XATTR_DEFAULT', 'XATTR_CREATE', 'XATTR_REPLACE']

"""
    LTTng Trace Input/Output Plotter
"""

BINARY_RETS = ['open', 'truncate', 'mkdir', 'chmod', 'close']

BYTES_RETS = ['read', 'write', 'lseek'] 

# without close
INPUT_PLOT_IGNORE = ['close']

OUTPUT_SYSCALLS = ['open', 'truncate', 'mkdir', 'chmod', 'close', 'read', 'write', 'lseek', 'chdir', 'setxattr', 'getxattr']

# 0 1 2 4 8 16 32 64 128 … 2^63, 2^64
# len(BOUNDARIES) == 66
# 63 intervals (66 - 1 - 2)
BOUNDARIES = [0] + [2 ** x for x in range(65)]

LOG2_XAXIS= [-1] + list(range(65))

# IOCov Analyzer

# O_CREAT (0100)|O_WRONLY (0001)|O_TRUNC (1000) 1101
CREAT_FLAG_DEC = 13

# Count the number of syscalls for IOCOV saving ratio and accuracy 
SC_COUNT_ARGS = {'open': 'mode', 
            'read': 'count',
            'write': 'count',
            'lseek': 'whence',
            'truncate': 'length',
            'mkdir': 'mode',
            'chmod': 'mode',
            'setxattr': 'size',
            'getxattr': 'size'
            }

# MCFS Specific

# MCFS_SYSCALLS handles:
# open [] write lseek truncate mkdir chmod
MCFS_SYSCALLS = {
    'create_file': ['open'], # 'close'
    'write_file': ['open', 'lseek', 'write'], # 'close'
    'truncate': ['truncate'],
    'mkdir': ['mkdir'],
    'chmod': ['chmod'],
    'setxattr': ['setxattr'],
    'getxattr': ['getxattr']
}

MCFS_WRITE_SIZE = [0,
                    3,
                    13,
                    555,
                    1021,
                    4001,
                    6144,
                    7790,
                    12288,
                    15567,
                    16355,
                    18432,
                    23344,
                    24576,
                    30720,
                    31121,
                    64409]

# Syzkaller Specific

# We are focusing on SYZKALLER_SYSCALLS related to file systems and supported by IOCov for now
# Note that readv, writev, preadv, pwritev, preadv2, pwritev2 are not handled
SYZKALLER_SYSCALLS = ['open', 'openat', 'creat', 'openat2', 
            'read', 'pread64', 'write', 'pwrite64',
            'lseek', 'llseek', 'truncate', 'ftruncate', 
            'mkdir', 'mkdirat', 'chmod', 'fchmod', 'fchmodat', 
            'close', 'close_range', 'chdir', 'fchdir', 
            'setxattr', 'lsetxattr', 'fsetxattr', 
            'getxattr', 'lgetxattr', 'fgetxattr']

# updated syscalls to calculate syzkaller input cov
SYZKALLER_SYSCALLS_NEW = ["open", "read", "write", "lseek", "close", 
                          "truncate", "unlink", "mkdir", "rmdir", "chmod", 
                          "chown", "setxattr", "removexattr", "getxattr", 
                          "rename", "link", "symlink", "statfs"]

ALL_SYSCALLS_NEW = SYZKALLER_SYSCALLS_NEW
SYZKALLER_HEADERS = {
    'open': ['syscall', 'pathname', 'flags', 'mode'],
    'openat': ['syscall', 'dirfd', 'pathname', 'flags', 'mode'],
    'creat': ['syscall', 'pathname', 'mode'],
    'openat2': ['syscall', 'dirfd', 'pathname', 'how', 'size'],
    'read': ['syscall', 'fd', 'buf', 'count'],
    'pread64': ['syscall', 'fd', 'buf', 'count', 'offset'],
    'write': ['syscall', 'fd', 'buf', 'count'],
    'pwrite64': ['syscall', 'fd', 'buf', 'count', 'offset'],
    'lseek': ['syscall', 'fd', 'offset', 'whence'],
    'llseek': ['syscall', 'fd', 'offset_high', 'offset_low', 'result', 'whence'],
    'truncate': ['syscall', 'path', 'length'],
    'ftruncate': ['syscall', 'fd', 'length'],
    'mkdir': ['syscall', 'pathname', 'mode'],
    'mkdirat': ['syscall', 'dirfd', 'pathname', 'mode'],
    'chmod': ['syscall', 'pathname', 'mode'],
    'fchmod': ['syscall', 'fd', 'mode'],
    'fchmodat': ['syscall', 'dirfd', 'pathname', 'mode', 'flags'],
    'close': ['syscall', 'fd'],
    'close_range': ['syscall', 'first', 'last', 'flags'],
    'chdir': ['syscall', 'path'],
    'fchdir': ['syscall', 'fd'],
    'setxattr': ['syscall', 'path', 'name', 'value', 'size', 'flags'],
    'lsetxattr': ['syscall', 'path', 'name', 'value', 'size', 'flags'],
    'fsetxattr': ['syscall', 'fd', 'name', 'value', 'size', 'flags'],
    'getxattr': ['syscall', 'path', 'name', 'value', 'size'],
    'lgetxattr': ['syscall', 'path', 'name', 'value', 'size'],
    'fgetxattr': ['syscall', 'fd', 'name', 'value', 'size'],
    'removexattr' : ['syscall', 'path', 'name'],
    'link' : ['syscall', 'oldpath', 'newpath'],
    'unlink' : ['syscall', 'pathname'],
    'symlink' : ['syscall', 'target' , 'linkpath'],
    'rmdir' : ['syscall', 'pathname'],
    'chown' : ['syscall', 'pathname', 'owner', 'group'],
    'rename' : ['syscall', 'oldpath', 'newpath'],
    'statfs' : ['syscall', 'path', 'buf']
}

# Those syscalls may have different numbers of arguments
SYZKALLER_ARGS_EXCEPTIONS = ['open', 'openat']

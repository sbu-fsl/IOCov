#!/bin/bash

#
# Copyright (c) 2020-2024 Yifei Liu
# Copyright (c) 2020-2024 Erez Zadok
# Copyright (c) 2020-2024 Stony Brook University
# Copyright (c) 2020-2024 The Research Foundation of SUNY
#
# You can redistribute it and/or modify it under the terms of the Apache License, 
# Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).
#

# Run this script with sudo

FS="ext4"
OPTION="allrecur"

CRASHMONKEY_DIR="/newdisk/yifei/crashmonkey-20230113/crashmonkey"

SYSCALLS=("open" "openat" "creat" "read" "pread64" "write" "pwrite64" "lseek" "llseek" "truncate" "ftruncate" "mkdir" "mkdirat" "chmod" "fchmod" "fchmodat" "close" "close_range" "chdir" "fchdir" "setxattr" "lsetxattr" "fsetxattr" "getxattr" "lgetxattr" "fgetxattr")

SUFFIX="crashmonkey-"
SCPARAM=""

for sc in ${SYSCALLS[@]}; do
    SCPARAM="${SCPARAM}${sc},"
done

SUFFIX="${SUFFIX}${FS}-${OPTION}"
# discard the last comma
SCPARAM="${SCPARAM::-1}"

cd $CRASHMONKEY_DIR
# rm -rf diff_results 

lttng create my-kernel-session-${SUFFIX} --output=/tmp/my-kernel-trace-${SUFFIX}

lttng enable-event --kernel --syscall $SCPARAM

start=`date +%s`

lttng start

# Run crashmonkey here
python xfsMonkey.py -f /dev/sda -d /dev/cow_ram0 -t $FS -e 102400 -u build/tests/ > outfile_${FS}_${OPTION}
mv diff_results diff_results_tests
mv outfile_${FS}_${OPTION} outfile_${FS}_${OPTION}_tests

python xfsMonkey.py -f /dev/sda -d /dev/cow_ram0 -t $FS -e 102400 -u build/tests/seq1/ > outfile_${FS}_${OPTION}
mv diff_results diff_results_seq1
mv outfile_${FS}_${OPTION} outfile_${FS}_${OPTION}_seq1

python xfsMonkey.py -f /dev/sda -d /dev/cow_ram0 -t $FS -e 102400 -u build/tests/generic_042/ > outfile_${FS}_${OPTION}
mv diff_results diff_results_generic_042
mv outfile_${FS}_${OPTION} outfile_${FS}_${OPTION}_generic_042

lttng stop

lttng destroy

chown -R $(whoami) /tmp/my-kernel-trace-${SUFFIX}

cd -

end=`date +%s`
runtime=$((end-start))

babeltrace2 /tmp/my-kernel-trace-${SUFFIX}/kernel > crashmonkey-lttng-${FS}-${OPTION}-${runtime}.log

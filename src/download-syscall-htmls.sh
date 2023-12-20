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

# Run this script to get the html files of syscall man pages in order
# to extract error codes for each system call

SYSCALLS=("open" "openat2" "read" "write" "lseek" "llseek" "truncate" "mkdir" "chmod" "close" "close_range" "chdir" "setxattr" "getxattr")

mkdir -p ./Assets/Html-Files/

for SC in "${SYSCALLS[@]}"
do
	wget https://man7.org/linux/man-pages/man2/${SC}.2.html -P ./Assets/Html-Files/
done

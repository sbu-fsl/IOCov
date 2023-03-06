#!/usr/bin/env python3

line_cnt = [143140, 143766, 145188, 146548, 147548, 149276, 149986, 151020, 151338, 151654]

line_cnt = [x - 1 for x in line_cnt]

example_path = 'syscall-async-examples.txt'

logname = '/mcfs2/LTTng-xfstests-2022-1211/IOCov/src/mcfs-lttng-mcfs-ext4-256-chdir-fchdir-10m-601.log'

cnt = 0
need_write_cnt = 0
need_write = False

with open(logname, 'r', encoding="utf8", errors='ignore') as file:
    for line in file:
        cnt += 1
        if cnt in line_cnt:
            need_write = True
            need_write_cnt = 0
            with open(example_path, 'a') as example_file:
                example_file.write(line)
            need_write_cnt += 1
        elif need_write:
            if need_write_cnt > 10:
                with open(example_path, 'a') as example_file:
                    example_file.write('==========\n')
                need_write = False 
                need_write_cnt = 0
            with open(example_path, 'a') as example_file:
                example_file.write(line)
            need_write_cnt += 1

print('All finished.')

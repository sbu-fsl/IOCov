#!/usr/bin/env python3

#
# Copyright (c) 2020-2024 Yifei Liu
# Copyright (c) 2020-2024 Erez Zadok
# Copyright (c) 2020-2024 Stony Brook University
# Copyright (c) 2020-2024 The Research Foundation of SUNY
#
# You can redistribute it and/or modify it under the terms of the Apache License, 
# Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).
#

from analyzerutils import *

def main():
    fig3_xfstests_filter_ratio = {}
    fig3_crashmonkey_filter_ratio = {}
    fig3_mcfs_filter_ratio = {}

    xfstests_unfilter_count = get_syscall_count_from_pkl('unfilter_input_cov_all_xfstests_xattrs.pkl')
    xfstests_filtered_count = get_syscall_count_from_pkl('input_cov_all_xfstests_xattrs.pkl')

    crashmonkey_unfilter_count = get_syscall_count_from_pkl('unfilter_input_cov_crashmonkey.pkl')
    crashmonkey_filtered_count = get_syscall_count_from_pkl('input_cov_crashmonkey.pkl')   

    mcfs_unfilter_count = get_syscall_count_from_pkl('unfilter_input_cov_mcfs_10m.pkl')
    mcfs_filtered_count = get_syscall_count_from_pkl('input_cov_mcfs_10m.pkl')       
    
    xfstests_total_filter_ratio = 0
    xfstests_total_filter = 0
    xfstests_total_unfilter = 0    

    crashmonkey_total_filter_ratio = 0
    crashmonkey_total_filter = 0
    crashmonkey_total_unfilter = 0

    mcfs_total_filter_ratio = 0
    mcfs_total_filter = 0
    mcfs_total_unfilter = 0

    for sc in SC_COUNT_ARGS.keys():
        if xfstests_filtered_count[sc] != 0:
            fig3_xfstests_filter_ratio[sc] = (xfstests_unfilter_count[sc] - xfstests_filtered_count[sc]) / xfstests_filtered_count[sc]
            xfstests_total_filter += xfstests_filtered_count[sc]
            xfstests_total_unfilter += xfstests_unfilter_count[sc]
        if crashmonkey_filtered_count[sc] != 0:
            fig3_crashmonkey_filter_ratio[sc] = (crashmonkey_unfilter_count[sc] - crashmonkey_filtered_count[sc]) / crashmonkey_filtered_count[sc]
            crashmonkey_total_filter += crashmonkey_filtered_count[sc]
            crashmonkey_total_unfilter += crashmonkey_unfilter_count[sc]
        if mcfs_filtered_count[sc] != 0:
            fig3_mcfs_filter_ratio[sc] = (mcfs_unfilter_count[sc] - mcfs_filtered_count[sc]) / mcfs_filtered_count[sc]
            mcfs_total_filter += mcfs_filtered_count[sc]
            mcfs_total_unfilter += mcfs_filtered_count[sc]

    with open('fig3_xfstests_filter_ratio.pkl', 'wb') as f:
        pickle.dump(fig3_xfstests_filter_ratio, f)
    with open('fig3_crashmonkey_filter_ratio.pkl', 'wb') as f:
        pickle.dump(fig3_crashmonkey_filter_ratio, f)
    with open('fig3_mcfs_filter_ratio.pkl', 'wb') as f:
        pickle.dump(fig3_mcfs_filter_ratio, f)

    print('fig3_xfstests_filter_ratio: ', fig3_xfstests_filter_ratio)
    print('fig3_crashmonkey_filter_ratio: ', fig3_crashmonkey_filter_ratio)
    print('fig3_mcfs_filter_ratio: ', fig3_mcfs_filter_ratio)
    print('======================')
    print('crashmonkey_total_unfilter - crashmonkey_total_filter: ', crashmonkey_total_unfilter - crashmonkey_total_filter)
    print('xfstests_total_unfilter - xfstests_total_filter: ', xfstests_total_unfilter - xfstests_total_filter)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

from analyzerutils import *

def main():
    save_ratio = {}

    unfilter_count = get_syscall_count_from_pkl('unfilter_input_cov_mcfs_10m.pkl')
    filtered_count = get_syscall_count_from_pkl('input_cov_mcfs_10m.pkl')

    print('unfilter_count: ', unfilter_count)
    print('filtered_count: ', filtered_count)
    
    for sc in SC_COUNT_ARGS.keys():
        save_ratio[sc] = (unfilter_count[sc] - filtered_count[sc]) / filtered_count[sc]

    print('save_ratio: ', save_ratio)

if __name__ == "__main__":
    main()

#!/bin/bash

METIS_STATE_DIR="/mcfs2/IOCov-experiments-2025-0312/metis-iocov-overhead-2025-0313/Metis/fs-state"
METIS_SCRIPT_DIR="/mcfs2/IOCov-experiments-2025-0312/metis-iocov-overhead-2025-0313/Metis/fs-state/mcfs_scripts"

ORIGINAL_DIR=$(pwd)

FS_TYPES=(ext4 xfs btrfs)
EXPCONFIG="with-iocov"
# One hour runtime by default
DURATION_SECONDS=3600

for FSTYPE in "${FS_TYPES[@]}"; do
    echo "EXP4 Metis overhead WITH IOCov for filesystem: $FSTYPE"
    cd $METIS_SCRIPT_DIR
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    ./only_one_fs_iocov_lttng.sh -f $FSTYPE -d $DURATION_SECONDS -e $EXPCONFIG -t $TIMESTAMP
    cd $METIS_STATE_DIR
    mkdir -p "iocov-overhead-$FSTYPE-$EXPCONFIG-${DURATION_SECONDS}secs-$TIMESTAMP"
    mv *.log *.csv *.gz *.txt "iocov-overhead-$FSTYPE-$EXPCONFIG-${DURATION_SECONDS}secs-$TIMESTAMP"
    cd "$ORIGINAL_DIR" || exit 1
done

echo "All completed for Metis IOCov $FSTYPE-$EXPCONFIG-${DURATION_SECONDS}!"

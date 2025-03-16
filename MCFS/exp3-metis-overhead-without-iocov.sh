#!/bin/bash

METIS_STATE_DIR="/mcfs2/IOCov-experiments-2025-0312/metis-iocov-overhead-2025-0313/Metis/fs-state"
METIS_SCRIPT_DIR="/mcfs2/IOCov-experiments-2025-0312/metis-iocov-overhead-2025-0313/Metis/fs-state/mcfs_scripts"

ORIGINAL_DIR=$(pwd)

FS_TYPES=(ext4 xfs btrfs)
EXPCONFIG="with-iocov"
# One hour runtime by default
RUNTIME_SECONDS=3600

for FSTYPE in "${FS_TYPES[@]}"; do
    echo "EXP3 Metis overhead WITHOUT IOCov for filesystem: $FSTYPE"
    cd $METIS_SCRIPT_DIR
    ./only_one_fs.sh $FSTYPE $RUNTIME_SECONDS
    cd $METIS_STATE_DIR
    mkdir -p "iocov-overhead-$FSTYPE-$EXPCONFIG-${RUNTIME_SECONDS}secs-$(date +%Y%m%d-%H%M%S)"
    mv *.log *.csv *.gz *.txt "iocov-overhead-$FSTYPE-$EXPCONFIG-${RUNTIME_SECONDS}secs-$(date +%Y%m%d-%H%M%S)"
    cd "$ORIGINAL_DIR" || exit 1
done

echo "All completed for Metis IOCov $FSTYPE-$EXPCONFIG-${RUNTIME_SECONDS}!"

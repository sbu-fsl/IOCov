#!/bin/bash

# Commands to use:
#  - python3 iocov-main.py <plot_name> --parse
#  - python3 iocov-main.py <plot_name> --no-parse --json
#  - python3 iocov-main.py <plot_name> --parse
#  - python3 iocov-main.py xfstests-ext4-generic-6569 --no-parse --json

# Metis:
# LTTNG_LOG_FILE="metis-lttng-all-related-metis-xfs-3600-with-iocov-20250321-154425-chdir-fchdir-3601.log"
# PLOT_NAME="metis-xfs-3600secs-iocov-20250321-154425"

################ LTTng log parse overhead ################

LTTNG_LOG_FILE="xfstests-lttng-all-related-syscalls-ext4-generic-with-iocov-chdir-fchdir-6569.log"
PLOT_NAME="xfstests-ext4-generic-6569"

RESULT_FILE="overhead-time-iocov-parse-$PLOT_NAME.log"

# Escape slashes for sed replacement
ESCAPED_LOG_FILE=$(printf '%s\n' "$LTTNG_LOG_FILE" | sed 's/[\&/]/\\&/g')

# Replace the line in iocov-main.py
sed -i.bak "s|^\( *\)default_lttng_log = '.*'|\1default_lttng_log = \"$ESCAPED_LOG_FILE\"|" iocov-main.py

# Get start time in nanoseconds
START_TIME_NS=$(date +%s%N)

# Run python script
python3 iocov-main.py $PLOT_NAME --parse

# Get end time in nanoseconds
END_TIME_NS=$(date +%s%N)

# Compute elapsed time in milliseconds
ELAPSED_NS=$((END_TIME_NS - START_TIME_NS))
ELAPSED_MS=$(echo "scale=3; $ELAPSED_NS / 1000000" | bc)
ELAPSED_SEC=$(echo "scale=3; $ELAPSED_NS / 1000000000" | bc)

# Write result to file
echo "Parse: ${ELAPSED_MS} milliseconds (${ELAPSED_SEC} seconds)" >> "$RESULT_FILE"

#!/bin/bash

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

# Write result to file
echo "Parse: ${ELAPSED_MS} milliseconds" >> "$RESULT_FILE"

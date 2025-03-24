#!/bin/bash

# Number of times to run the script
NUM_RUNS=10  

TARGET_SCRIPT="./exp3-metis-overhead-without-iocov.sh"  

# Optional: use command-line argument to override NUM_RUNS
if [ ! -z "$1" ]; then
  NUM_RUNS=$1
fi

# Loop to run the script multiple times
for ((i=1; i<=NUM_RUNS; i++))
do
  echo "Running $TARGET_SCRIPT (Run $i of $NUM_RUNS)"
  bash "$TARGET_SCRIPT"
done

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

set -e

# Let's always use "-" as the separator (not "_")

# mkdir WHM-inverse-40mins-open-flags-20230816-191040-861324
# mv *.log *.csv *.gz *.txt WHM-inverse-40mins-open-flags-20230816-191040-861324

# SEQFILE=/mcfs/iocov-mcfs-fast24-2023-0723/nfs4mc/driver-fs-state/WHM-inverse-40mins-open-flags-20230817-024926-918867/sequence-pan-20230817-024926-918867.log

# SEQFILE=/mcfs/iocov-mcfs-fast24-2023-0723/nfs4mc/driver-fs-state/IRZD-4hours-33parts-90p-write-size-20230907-203157-1594068/sequence-pan-20230907-203157-1594068.log

SEQFILE=/mcfs/iocov-mcfs-fast24-2023-0723/nfs4mc/driver-fs-state/IRSD-40minutes-33parts-90p-write-sizes-20230913-042245-3004566/sequence-pan-20230913-042245-3004566.log

SUFFIX=$(echo $SEQFILE | rev | cut -d'/' -f2 | rev)
FILENAME=$SUFFIX".log"


#################### Section 1: Parse the sequence file ####################
# echo "FILENAME: $FILENAME"

# Copy the sequence file to the current directory
cp $SEQFILE ./$FILENAME

# Parge the sequence file and get the pickle/json file for the input coverage
# E.g., we can get input-cov-mcfs-WHM-inverse-40mins-open-flags-20230816-191040-861324.pkl
# and input-cov-mcfs-WHM-inverse-40mins-open-flags-20230816-191040-861324.json
python3 parser-mcfs-log-input.py $FILENAME

PKLNAME="input-cov-mcfs-"$SUFFIX".pkl"

#################### Section 2: Plot input coverage roughly and get the input coords as pkl files ####################

# Ex.: input-cov-mcfs-WHM-inverse-40mins-open-flags-20230816-191040-861324.pkl
# echo "PKLNAME: $PKLNAME"
cp $PKLNAME ../src
cd ../src
cp $PKLNAME unfilter-$PKLNAME

# Plot the input coverage and get the input coords as pkl files

python3 iocov-main.py $PKLNAME --no-parse --plot -i

echo "All completed!"

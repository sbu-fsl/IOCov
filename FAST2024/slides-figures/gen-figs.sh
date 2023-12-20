#!/bin/sh

#
# Copyright (c) 2020-2024 Yifei Liu
# Copyright (c) 2020-2024 Erez Zadok
# Copyright (c) 2020-2024 Stony Brook University
# Copyright (c) 2020-2024 The Research Foundation of SUNY
#
# You can redistribute it and/or modify it under the terms of the Apache License, 
# Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).
#

# Generate figures for FMitF-VeriFS-HotOS-2021 paper

# Usage: edit downloed FMITF-NFS-HotOS2021-Figures.pdf from google slides
# into your ~/Downloads folder:
#
# https://docs.google.com/presentation/d/1GgvD26xV0EiCM5IkGUwPzbV9hj9XO2I6UMFAwsW89kI/edit#slide=id.gae142d6554_0_422
#
# Then update this script.  Add new entries here to extract more figs.  Then
# run this script.

# Run by "bash gen-figs.sh"

# SRC="IOCov-HotStorage23-Figures.pdf"

SRC="ALL-FMITF-METIS-Figures.pdf"
# SRC="Metis-FAST24-Two-Column-Wide-Figures.pdf"

# ARGS: pagenum fig-name-you-want.pdf
# generates "fig-name-you-want-ann.pdf" (ANNotated)
function get1fig
{
    n=`basename "$2" .pdf`
    qpdf --empty --pages "$SRC" $1-$1 -- temp.pdf || exit $?
    pdfcrop temp.pdf || exit $?
    mv temp-crop.pdf ${n}.pdf || exit $?
}

if test -f "${HOME}/Downloads/$SRC" ; then
    mv -v "${HOME}/Downloads/$SRC" .
fi

# HotStorage'23 IOCov

# IOCov Architecture figure
# get1fig 1 iocov-framework.pdf
# IOCov Bug Example Figure
# get1fig 2 bug-example.pdf

# FAST'24 Metis and RefFS

# Metis Architecture figure
get1fig 29 metis-arch-one-col.pdf
# RefFS Architecture figure
get1fig 30 reffs-arch.pdf
# Input Driver Weights figure
get1fig 31 input-weights.pdf
# Swarm Example figure
get1fig 32 swarm-example.pdf
# Simple state exploration figure
get1fig 33 state-exploration-one-col.pdf

# State exploration two-column wide figure
# get1fig 1 state-exploration.pdf
# get1fig 3 metis-arch-two-cols.pdf

# cleanup
rm -f temp.pdf

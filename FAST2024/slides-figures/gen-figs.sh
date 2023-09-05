#!/bin/sh
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
get1fig 28 metis-arch.pdf
# RefFS Architecture figure
get1fig 29 reffs-arch.pdf

# State exploration two-column wide figure
# get1fig 1 state-exploration.pdf

# cleanup
rm -f temp.pdf
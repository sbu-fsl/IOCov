#!/bin/sh
# Generate figures for FMitF-VeriFS-HotOS-2021 paper

# Usage: edit downloed FMITF-NFS-HotOS2021-Figures.pdf from google slides
# into your ~/Downloads folder:
#
# https://docs.google.com/presentation/d/1GgvD26xV0EiCM5IkGUwPzbV9hj9XO2I6UMFAwsW89kI/edit#slide=id.gae142d6554_0_422
#
# Then update this script.  Add new entries here to extract more figs.  Then
# run this script.

SRC="FMITF-NFS-HotOS2021-Figures.pdf"

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
# model checking high level arch figure
get1fig 1 mc-framework.pdf
# problems we discovered trying to MC file systems figure
get1fig 2 filesystems-workflow.pdf
# verifs arch fig
get1fig 3 verifs-architecture.pdf

# cleanup
rm -f temp.pdf

#!/bin/bash

# construct_cdls.sh
# =================
#
# Reads ACTIVE FILES and creates a cdl for each inside 'cdls/'
# directory.
#

while read NC; do
    if [[ ! $NC =~ "dat" ]]; then
        base=$(echo $NC | sed 's/\.nc//g')
        cdl=cdls/$(basename $base).cdl
        echo "Generating: $cdl"
        ncdump $NC > $cdl 
    fi
done < ACTIVE_FILES.txt

#!/bin/bash

# remake_ncs_from_cdls.sh
# =======================
#
# Writes NC files from CDL files.
#

while read NC; do
    if [[ ! $NC =~ "dat" ]]; then
        base=$(echo $NC | sed 's/\.nc//g')
        cdl=cdls/$(basename $base).cdl
        echo "Generating: $NC"
        ncgen -o $NC $cdl 
    fi
done < ACTIVE_FILES.txt

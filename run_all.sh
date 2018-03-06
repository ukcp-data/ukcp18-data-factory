#!/bin/bash

. setup_env.sh

recipes=$(ls recipes/ukcp18/ukcp18-land-*)

for recipe in $recipes; do
    echo "Running for: $recipe"
    python create_dataset.py --three-only $recipe

    if [ $? -ne 0 ]; then
        echo "Failed on: $recipe"
        exit
    fi
done

#!/usr/bin/env bash

BUILDS=()

mapfile -t BUILDS < <(find fonts -mindepth 1 -type d -not -path fonts/ignore | perl -p -e "s/fonts\///g")

for item in "${BUILDS[@]}"; do
    ./scripts/generate_build.sh "$item"
done
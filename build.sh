#!/usr/bin/env bash

shopt -s globstar

builds=(fonts/**/build.sh)

printf "Building %d font families\n" ${#builds[@]}
rm -rf output
for b in "${builds[@]}"; do
    "$b"
done
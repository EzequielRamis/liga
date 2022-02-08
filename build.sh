#!/usr/bin/env bash

shopt -s globstar

pushd $(dirname "$0") || exit

builds=(fonts/**/build.sh)

printf "Building %d font families\n" ${#builds[@]}
scripts/clean.sh
for b in "${builds[@]}"; do
    "$b"
done

popd || exit

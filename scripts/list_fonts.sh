#!/usr/bin/env bash

shopt -s globstar

if [ "$(command -v exa)" ]; then
    exa -l -s mod -r fonts/**/build.sh
else
    ls -l --sort time fonts/**/build.sh
fi

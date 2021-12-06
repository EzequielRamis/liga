#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

pushd "$SCRIPT_DIR" || exit
    mkdir -p /ush/share/fonts/liga-test
    cp ../output/* /ush/share/fonts/liga-test/
    fc-cache -vf
popd || exit
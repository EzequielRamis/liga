#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

pushd "$SCRIPT_DIR" || exit
    mkdir -p /usr/share/fonts/liga-test
    cp ../output/* /usr/share/fonts/liga-test/
    fc-cache -vf
popd || exit
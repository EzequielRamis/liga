#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

pushd "$SCRIPT_DIR" || exit
        
    ./test/fetch_fonts_data.sh > /dev/null

    python3 -m http.server

popd || exit
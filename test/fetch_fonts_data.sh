#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

pushd "$SCRIPT_DIR/.." || exit
    echo 'var fonts = `' > test/fonts.js
    printf "<option value='%s'>%s</option>\n" \
        $(fc-scan output/ -f "%{postscriptname} %{postscriptname}\n") \
        >> test/fonts.js
    echo '`;' >> test/fonts.js

    printf "@font-face {font-family:'%s';src:url('../%s');font-weight:normal;font-style:normal}\n" \
        $(fc-scan output/ -f "%{postscriptname} %{file}\n") \
        > test/fonts.css
popd || exit
#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo 'var show = `' > "$SCRIPT_DIR"/showcases.js
curl https://raw.githubusercontent.com/tonsky/FiraCode/master/extras/showcases.txt >> "$SCRIPT_DIR"/showcases.js
echo '`;' >> "$SCRIPT_DIR"/showcases.js
#!/usr/bin/env bash

./test/fetch_fonts_data.sh > /dev/null

python3 -m http.server
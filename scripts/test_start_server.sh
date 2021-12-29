#!/usr/bin/env bash

scripts/test_fonts_data.sh > /dev/null

python3 -m http.server
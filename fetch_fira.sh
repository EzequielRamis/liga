#!/usr/bin/env bash

version=6

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
tmpDir=$(mktemp -d)

wget "https://github.com/tonsky/FiraCode/releases/download/$version/Fira_Code_v$version.zip" \
    -O "$tmpDir/fira.zip"
7z x -o"$tmpDir" "$tmpDir/fira.zip"

rm -rf "$SCRIPT_DIR/fira"
mv "$tmpDir/ttf" "$SCRIPT_DIR/fira"

rm -rf "$tmpDir"
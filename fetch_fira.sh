#!/usr/bin/env bash

version=6

repDir=$(realpath "$(dirname "$(BASH_SOURCE)")")
tmpDir=$(mktemp -d)

wget "https://github.com/tonsky/FiraCode/releases/download/$version/Fira_Code_v$version.zip" \
    -O "$tmpDir/fira.zip"
7z x -o"$tmpDir" "$tmpDir/fira.zip"

rm -rf "$repDir/fira"
mv "$tmpDir/ttf" "$repDir/fira"

rm -rf "$tmpDir"
#!/usr/bin/env bash

version=6

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
tmpDir=$(mktemp -d)

pushd "$SCRIPT_DIR" || exit

wget "https://github.com/tonsky/FiraCode/releases/download/$version/Fira_Code_v$version.zip" \
    -O "$tmpDir/fira.zip"
7z x -o"$tmpDir" "$tmpDir/fira.zip"

rm -rf ./fira/*
mv "$tmpDir"/ttf/* ./fira/

rm -rf "$tmpDir"

wget "https://raw.githubusercontent.com/tonsky/FiraCode/$version/FiraCode.glyphs" \
    -O ./fira.glyphs

for f in ./fira/*.ttf; do
    fo=$(basename "$f" .ttf)
    fontforge -quiet -lang=ff -c "Open('$f'); Generate('./fira/$fo.otf'); Close();"
done

popd || exit
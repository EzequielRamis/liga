#!/usr/bin/env bash

pushd output || exit
zip -r Liga_Fonts_v"$1".zip . -x "ignore/*"
popd || exit
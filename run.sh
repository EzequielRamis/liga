#!/usr/bin/env bash

fontforge -lang py -script ligaturize.py input/SF-Mono-Regular.otf \
                    --ligature-font-file fira/FiraCode-Regular.otf \
                    --scale-fira-glyphs 1 \
                    --output-dir output
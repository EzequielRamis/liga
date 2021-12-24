#!/usr/bin/env bash

fontforge -lang py -script ligate.py input/FreeMono.otf \
                    --ligature-font-file fira/FiraCode-Regular.otf \
                    --output-dir output
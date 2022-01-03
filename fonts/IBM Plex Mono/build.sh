#!/usr/bin/env bash

# You can ignore these two lines
source ./scripts/build_family.sh
declare -A FONT_WEIGHT

# PREFIX="Liga "
OUTPUT_NAME="Liga IBM Flex Mono"

INPUT_DIR="IBM Plex Mono"
CONFIG="fonts/IBM Plex Mono/config.py"

# The variable below is a associative array in which keys must be the basename
# of each font file (without extensions), and values the following options:
# - Light
# - Regular
# - Retina
# - Medium
# - SemiBold
# - Bold
# This serves the purpose of handwrite the weight of the firacode file in case
# the automatic weight detection doesn't fit well.

FONT_WEIGHT=(
    # Example
    # ["IBMPlexMono-Thin"]="Light"
    # ["IBMPlexMono-Regular"]="Regular"
    # ["IBMPlexMono-Text"]="Retina"
    # ["IBMPlexMono-Bold"]="Bold"
)

# If this variable is set to true, only the files specified in $FONT_WEIGHT
# will be ligated. Otherwise, all the font files will also be.
FILTER_BY_FONT_WEIGHT=false

COPY_GLYPHS=true
REMOVE_ORIGINAL_LIGATURES=false

build_family

# That's all. Finally you could copy the font license to the output
# directory, like:
cp "input/IBM Plex Mono/LICENSE.txt" "output/$OUTPUT_NAME/"

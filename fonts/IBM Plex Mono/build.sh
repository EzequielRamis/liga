#!/usr/bin/env bash

# You can ignore these two lines
source ./scripts/build_family.sh
declare -A FONT_WEIGHT

# String to prefix the name of the generated font with.
# PREFIX="Liga "

# Name of the generated font. Completely replaces the original and prefix
# variable will be ignored.
OUTPUT_NAME="Liga Flex Mono"

# Where the input font files are located
INPUT_DIR="IBM Plex Mono"

# The python file to copy the configuration from.
CONFIG="fonts/IBM Plex Mono/config.py"

# The variable below is a associative array in which keys must be the basename
# of each font file (without extensions), and values the following options:
# - Light
# - Regular
# - Retina
# - Medium
# - SemiBold
# - Bold
# This serves the purpose of handwrite the weight of the FiraCode file in case
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

# Copy glyphs for (some) individual characters from the ligature font as well.
# This will result in punctuation that matches the ligatures more closely, but
# may not fit in as well with the rest of the font.
COPY_GLYPHS=true

# Remove the currently existing ligatures from the input font file. It is
# recommended in case of glitches present in the resulting font.
REMOVE_ORIGINAL_LIGATURES=true

build_family

# Finally you could copy the font license to the output
# directory, like:
cp "input/IBM Plex Mono/LICENSE.txt" "output/$OUTPUT_NAME/"

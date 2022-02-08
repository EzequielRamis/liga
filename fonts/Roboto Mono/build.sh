#!/usr/bin/env bash

SRC=$(dirname "${BASH_SOURCE[0]}")

# Project root path relative to this .sh file
LIGA_DIR=$SRC/../..
SCRIPTS_DIR=$LIGA_DIR/scripts
source "$SCRIPTS_DIR"/build_family.sh
declare -A FONT_WEIGHT

# String to prefix the name of the generated font with.
PREFIX="Liga "

# Name of the generated font. Completely replaces the original and prefix
# variable will be ignored.
# OUTPUT_NAME=""

# Where the generated font files will be located
OUTPUT_DIR="$LIGA_DIR/output/$PREFIX""Roboto Mono"

# Where the input font files are located
INPUT_DIR="$LIGA_DIR/input/Roboto Mono"

# The python file to copy the configuration from.
CONFIG="$SRC/config.py"

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
# recommended in case of glitches presented in the resulting font.
REMOVE_ORIGINAL_LIGATURES=true

pushd "$LIGA_DIR" || exit
    build_family
popd || exit

# Finally you could copy the font license to the output
# directory, like:
cp "$INPUT_DIR/LICENSE.txt" "$OUTPUT_DIR"

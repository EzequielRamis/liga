#!/usr/bin/env bash

# shellcheck source=/dev/null
source ./scripts/build_family.sh

FAMILY="IBM Plex Mono"
PREFIX="Liga "
# OUTPUT_NAME=""

INPUT_DIR="$FAMILY"
EXT="otf"

declare -A fontWeight

# Available weight options:
# - Light
# - Regular
# - Retina
# - Medium
# - SemiBold
# - Bold

fontWeight=(
    ["IBMPlexMono-Light"]="Light"
    ["IBMPlexMono-Regular"]="Regular"
    ["IBMPlexMono-Medium"]="Medium"
    ["IBMPlexMono-Bold"]="Bold"
)

build_family "$INPUT_DIR" "$(declare -p fontWeight)" $EXT "$PREFIX" "$OUTPUT_NAME"
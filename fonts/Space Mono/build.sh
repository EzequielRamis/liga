#!/usr/bin/env bash

# shellcheck source=/dev/null
source ./scripts/build_family.sh

FAMILY="Space Mono"
PREFIX="Liga "
# OUTPUT_NAME=""

INPUT_DIR="$FAMILY"
EXT="ttf"

declare -A fontWeight

# Available weight options:
# - Light
# - Regular
# - Retina
# - Medium
# - SemiBold
# - Bold

fontWeight=(
    ["SpaceMono-Regular"]="Regular"
    ["SpaceMono-Bold"]="Bold"
)

build_family "$INPUT_DIR" "$(declare -p fontWeight)" $EXT "$PREFIX" "$OUTPUT_NAME"
#!/usr/bin/env bash

# shellcheck source=/dev/null
source ./scripts/build_family.sh

FAMILY="Space Mono"
PREFIX="Liga "
SUFFIX=""
# OUTPUT_NAME=""

DIR="$FAMILY"
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

if [[ -z "$OUTPUT_NAME" ]]; then
    OUTPUT_NAME="$PREFIX$FAMILY$SUFFIX"
fi

build_family "$DIR" "$(declare -p fontWeight)" $EXT "$OUTPUT_NAME"
#!/usr/bin/env bash

# shellcheck source=/dev/null
source ./scripts/build_family.sh

FAMILY="IBM Plex Mono"
PREFIX="Liga "
SUFFIX=""
# OUTPUT_NAME=""

DIR="$FAMILY"
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
    ["IBMPlexMono-Regular"]="Regular"
    ["IBMPlexMono-Medium"]="Medium"
    ["IBMPlexMono-Bold"]="Bold"
)

if [[ -z "$OUTPUT_NAME" ]]; then
    OUTPUT_NAME="$PREFIX$FAMILY$SUFFIX"
fi

build_family "$DIR" "$(declare -p fontWeight)" $EXT "$OUTPUT_NAME"
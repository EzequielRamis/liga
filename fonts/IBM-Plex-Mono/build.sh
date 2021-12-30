#!/usr/bin/env bash

# shellcheck source=/dev/null
source ./scripts/build_family.sh

# DIR=""
DIR="IBM-Plex-Mono"
PREFIX="Liga "
SUFFIX=""

declare -A fontWeight

# Available weight options:
# - Light
# - Regular
# - Retina
# - Medium
# - SemiBold
# - Bold

fontWeight=(
    ["IBMPlexMono-Medium"]="Medium"
    ["IBMPlexMono-Regular"]="Regular"
    ["IBMPlexMono-Bold"]="Bold"
)

build_family "$DIR" "$(declare -p fontWeight)" "otf" "$PREFIX" "$SUFFIX"
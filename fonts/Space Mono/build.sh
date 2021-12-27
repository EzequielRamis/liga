#!/usr/bin/env bash

# shellcheck source=/dev/null
source ./scripts/build_family.sh

# DIR=""
DIR="Space Mono"

declare -A fontWeight

# Available weight options:
# - Light
# - Regular
# - Retina
# - Medium
# - SemiBold
# - Bold

fontWeight=(
    ["SpaceMono-Bold"]="Bold"
    ["SpaceMono-Regular"]="Regular"
)

build_family "$DIR" "$(declare -p fontWeight)" "ttf"
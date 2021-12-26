#!/usr/bin/env bash

# DIR=""
DIR="Space_Mono"

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

insert() {
    { echo "$1"; cat "$2" 2> /dev/null; } >"$2".new
    mv "$2"{.new,}
}

ligate_ext() {
    local ext="$1"
    for file in ./input/"$DIR"/**."$ext"; do
        b=$(basename "$file" ."$ext")
        w=${fontWeight["$b"]}
        if [[ -n "$w" ]]; then
            ERROR=$(fontforge -quiet -lang py -script ligate.py "$file" \
                    --ligature-font-file "fira/FiraCode-$w.$ext" \
                    --output-dir output/"$DIR" 3>&1 1>&2 2>&3)
            if [[ -n "$ERROR" ]]; then
                LOG="logs/$DIR/$b.$ext.log"
                insert "" "$LOG"
                insert "$ERROR" "$LOG"
                insert "[$(date -R)]" "$LOG"
            fi
        fi
    done
}

if [ -d ./input/"$DIR" ]; then
    mkdir -p output/"$DIR"
    mkdir -p logs/"$DIR"
    ligate_ext "otf"
    ligate_ext "ttf"
else
    echo "Error: directory ./input/$DIR does not exist"
fi
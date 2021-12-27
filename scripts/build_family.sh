#!/usr/bin/env bash

# Source progress bar
# shellcheck source=/dev/null
source ./scripts/progress_bar.sh

insert_top() {
    { echo "$1"; cat "$2" 2> /dev/null; } >"$2".new
    mv "$2"{.new,}
}

build_family() {
    local DIR=$1
    eval "declare -A FONT_WEIGHT=""${2#*=}"
    local EXT=$3
    if [ -d "./input/$DIR" ]; then
        mkdir -p "output/$DIR"
        files=("./input/$DIR/"*."$EXT")
        filtered_files=()
        for file in "${files[@]}"; do
            b=$(basename "$file" ."$EXT")
            w=${FONT_WEIGHT["$b"]}
            if [[ -n "$w" ]]; then
                filtered_files+=("$file")
            fi
        done
        total=${#filtered_files[@]}
        setup_scroll_area "$total"
        printf "Found %d fonts from %s directory to be ligated\n" "$total" "$DIR"
        for ((k = 0; k < total ; k++)); do
            draw_progress_bar "$k"
            echo ""
            file=${filtered_files[$k]}
            b=$(basename "$file")
            ERROR=$(fontforge -quiet -lang py -script ligate.py "$file" \
                    --ligature-font-file "fira/FiraCode-$w.$EXT" \
                    --copy-character-glyphs \
                    --output-dir "output/$DIR" 3>&1 1>&2 2>&3)
            if [[ -n "$ERROR" ]]; then
                mkdir -p "logs/$DIR"
                LOG="logs/$DIR/$b.log"
                insert_top "" "$LOG"
                insert_top "$ERROR" "$LOG"
                insert_top "[$(date -R)]" "$LOG"
            fi
        done
        destroy_scroll_area
        print_bar_text "$total"; echo ""
    else
        echo "Error: directory ./input/$DIR does not exist"
        exit 1
    fi
}

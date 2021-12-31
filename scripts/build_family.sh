#!/usr/bin/env bash

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
    local PREFIX="$4"
    local OUTPUT_NAME="$5"

    if [[ -z "$OUTPUT_NAME" ]]; then
       ARGS="--prefix '$PREFIX'"
       OUTPUT_DIR="$(dirname "$DIR")/$PREFIX$(basename "$DIR")"
       OUTPUT_DIR="${OUTPUT_DIR/.\/}"
    else
       ARGS="--output-name '$OUTPUT_NAME'"
       OUTPUT_DIR="$OUTPUT_NAME"
    fi

    if [ -d "./input/$DIR" ]; then
        rm -rf "output/$DIR"
        mkdir -p "output/$OUTPUT_DIR"
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
        printf "\nFound %d fonts from %s directory to be ligated\n" "$total" "$DIR"
        for ((k = 0; k < total ; k++)); do
            draw_progress_bar "$k"
            file=${filtered_files[$k]}
            b=$(basename "$file" ."$EXT")
            w=${FONT_WEIGHT["$b"]}
            local attempt=1
            while (( $(find "output/$OUTPUT_DIR" -type f | wc -l) <= k )); do
                echo ""
                if (( attempt > 1 )); then
                    echo -e "Fontforge has a bad day... attempt #$attempt\n"
                fi
                ERROR=$(eval "fontforge -quiet -lang py -script ligate.py '$file' --ligature-font-file 'fira/FiraCode-$w.$EXT' --output-dir 'output/$OUTPUT_DIR' --copy-character-glyphs" "$ARGS" 3>&1 1>&2 2>&3)
                if [[ -n "$ERROR" ]]; then
                    mkdir -p "logs/$DIR"
                    LOG="logs/$DIR/$b.$EXT.log"
                    insert_top "" "$LOG"
                    insert_top "$ERROR" "$LOG"
                    insert_top "[$(date -R)]" "$LOG"
                fi
                # shellcheck disable=SC2126
                ERROR_COUNT=$(echo -n "$ERROR" | grep -A1 '====' | wc -l)
                if (( ERROR_COUNT > 1)); then
                    printf "\n \033[0;31m✗\033[0m There are some errors saved at %s\n" "$LOG"
                else 
                    echo -e "\n \033[0;32m✓\033[0m Font ligated"
                fi
                ((attempt=attempt+1))
            done
        done
        destroy_scroll_area
        print_bar_text "$total"; echo ""
    else
        echo "Error: directory ./input/$DIR does not exist"
        exit 1
    fi
}

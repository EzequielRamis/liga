#!/usr/bin/env bash

# shellcheck source=/dev/null
source ./scripts/progress_bar.sh
shopt -s extglob

declare -A CSS_WEIGHTS

# from fc-scan weight to css font-weight
CSS_WEIGHTS=(
    ["0"]="100" # thin
    ["40"]="200" # extra light
    ["50"]="300" # light
    ["80"]="400" # regular
    ["90"]="450" # retina
    ["100"]="500" # medium
    ["180"]="600" # semi bold
    ["200"]="700" # bold
    ["210"]="900" # black
)

insert_top() {
    { echo "$1"; cat "$2" 2> /dev/null; } >"$2".new
    mv "$2"{.new,}
}

build_family() {
    if [[ -z "$OUTPUT_NAME" ]]; then
       ARGS="--prefix '$PREFIX'"
       OUTPUT_DIR="$(dirname "$INPUT_DIR")/$PREFIX$(basename "$INPUT_DIR")"
       OUTPUT_DIR="${OUTPUT_DIR/.\/}"
    else
       ARGS="--output-name '$OUTPUT_NAME'"
       OUTPUT_DIR="$OUTPUT_NAME"
    fi

    if [[ -n "$CONFIG" ]]; then
       ARGS="$ARGS --config-file '$CONFIG'"
    fi

    if [ -d "./input/$INPUT_DIR" ]; then
        mkdir -p "output/$OUTPUT_DIR"
        files=(./input/"$INPUT_DIR"/*.+(ttf|otf))
        filtered_files=()
        if $FILTER_BY_FONT_WEIGHT; then
            for file in "${files[@]}"; do
            b=$(basename "$file" ".ttf")
            b=$(basename "$b" ".otf")
            w=${FONT_WEIGHT["$b"]}
            if [[ -n "$w" ]]; then
                filtered_files+=("$file")
            fi
        done
        else
            for file in "${files[@]}"; do
                filtered_files+=("$file")
            done
        fi
        total=${#filtered_files[@]}
        setup_scroll_area "$total"
        printf "\nFound %d fonts from %s directory to be ligated ✨\n" "$total" "$INPUT_DIR"
        for ((k = 0; k < total ; k++)); do
            draw_progress_bar "$k"
            file=${filtered_files[$k]}
            b=$(basename "$file" ".ttf")
            b=$(basename "$b" ".otf")
            w=${FONT_WEIGHT["$b"]}
            EXT="${file##*.}"
            if [[ -n "$w" ]]; then
                LIGATURE="--ligature-font-file 'fira/FiraCode-$w.$EXT'"
            else
                LIGATURE=""
            fi
            local attempt=1
            while (( $(find "output/$OUTPUT_DIR" -regex ".+\.\(otf\|ttf\)" -type f | wc -l) <= k )); do
                echo ""
                if (( attempt > 1 )); then
                    echo -e "Fontforge has a bad day... attempt #$attempt\n"
                fi
                ERROR=$(eval "fontforge -quiet -lang py -script ligate.py '$file' \
                                --output-dir 'output/$OUTPUT_DIR' \
                                --copy-character-glyphs" \
                                "$LIGATURE" "$ARGS" 3>&1 1>&2 2>&3)
                if [[ -n "$ERROR" ]]; then
                    mkdir -p "logs/$INPUT_DIR"
                    LOG="logs/$INPUT_DIR/$b.$EXT.log"
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

            # Add font data to the Font Tester .html page
            OUTPUT_FILE=$(ls -Art "output/$OUTPUT_DIR" | tail -n 1)
            COMPL_OUT_FILE="output/$OUTPUT_DIR/$OUTPUT_FILE"
            POST=$(fc-scan "$COMPL_OUT_FILE" -f "%{postscriptname}")
            FULL=$(fc-scan "$COMPL_OUT_FILE" -f "%{fullname}")
            CSS_WEIGHT=${CSS_WEIGHTS[$(fc-scan "$COMPL_OUT_FILE" -f "%{weight}")]}
            echo -e "<option value=\"$CSS_WEIGHT 16px '$POST'\">$FULL</option>" \
                >> test/fonts.html

            echo "@font-face {font-family:'$POST';src:url('../$COMPL_OUT_FILE');font-weight:$CSS_WEIGHT;font-style:italic}" \
                >> test/fonts.css

            echo "@font-face {font-family:'$POST';src:url('../$file');font-weight:$CSS_WEIGHT;font-style:normal}" \
                >> test/fonts.css

        done
        destroy_scroll_area
        print_bar_text "$total"; echo ""
    else
        echo "Error: directory ./input/$INPUT_DIR does not exist"
        exit 1
    fi
}

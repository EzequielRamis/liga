#!/usr/bin/env bash

shopt -s globstar

declare -A WEIGHT

# from fc-scan weight to css font-weight
WEIGHT=(
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

echo 'var fonts = `' > test/fonts.js
echo "" > test/fonts.css
for f in output/**/*; do
    if [ -f "$f" ]; then
        post=$(fc-scan "$f" -f "%{postscriptname}")
        full=$(fc-scan "$f" -f "%{fullname}")
        path=$(fc-scan "$f" -f "%{file}")
        w=${WEIGHT[$(fc-scan "$f" -f "%{weight}")]}

        echo -e "<option value=\"$w 16px '$post'\">$full</option>" \
            >> test/fonts.js

        echo "@font-face {font-family:'$post';src:url('../$path');font-weight:$w;font-style:normal}" \
            >> test/fonts.css
    fi
done
echo '`;' >> test/fonts.js
#!/usr/bin/env bash

shopt -s globstar

declare -A WEIGHT

# from fc-scan weight to css font-weight
WEIGHT=(
    ["0"]="100"
    ["40"]="200"
    ["50"]="300"
    ["80"]="400"
    ["90"]="450"
    ["100"]="500"
    ["180"]="600"
    ["200"]="700"
    ["210"]="900"
)

echo 'var fonts = `' > test/fonts.js
echo "" > test/fonts.css
for f in output/**/*; do
    if [ -f "$f" ]; then
        post=$(fc-scan "$f" -f "%{postscriptname}")
        path=$(fc-scan "$f" -f "%{file}")
        w=${WEIGHT[$(fc-scan "$f" -f "%{weight}")]}

        echo -e "<option value=\"$w 16px '$post'\">$post</option>" \
            >> test/fonts.js

        echo "@font-face {font-family:'$post';src:url('../$path');font-weight:$w;font-style:normal}" \
            >> test/fonts.css
    fi
done
echo '`;' >> test/fonts.js
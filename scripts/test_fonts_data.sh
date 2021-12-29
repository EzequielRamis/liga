#!/usr/bin/env bash

declare -A WEIGHT

# from fc-scan weight to css font-weight
WEIGHT=(
    ["50"]="300"
    ["80"]="400"
    ["90"]="450"
    ["100"]="500"
    ["180"]="600"
    ["200"]="700"
)

echo 'var fonts = `' > test/fonts.js
echo "" > test/fonts.css
for f in output/*/*; do
    post=$(fc-scan "$f" -f "%{postscriptname}")
    path=$(fc-scan "$f" -f "%{file}")
    w=${WEIGHT[$(fc-scan "$f" -f "%{weight}")]}

    echo -e "<option value=\"$w 16px '$post'\">$post</option>" \
        >> test/fonts.js

    echo "@font-face {font-family:'$post';src:url('../$path');font-weight:$w;font-style:normal}" \
        >> test/fonts.css

done
echo '`;' >> test/fonts.js
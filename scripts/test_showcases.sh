#!/usr/bin/env bash

echo 'var show = `' > test/showcases.js
curl https://raw.githubusercontent.com/tonsky/FiraCode/master/extras/showcases.txt >> test/showcases.js
echo '`;' >> test/showcases.js
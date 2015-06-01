#!/usr/local/bin/bash

echo $1
mkdir -p ./$1


cat $1 "${1}-labs" | while read line
do 
	echo "http://www.rockefeller.edu/research/faculty/labheads/$line" | wget -O- -i- | hxnormalize -x  | lynx -stdin -dump -nonumbers -hiddenlinks=ignore > ./$1/$line
done

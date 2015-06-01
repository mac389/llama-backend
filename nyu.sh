#!/usr/local/bin/bash

echo "Scraping $1"

#Each institute of NYU has its own organization, prototyped with Biology

#Scrape NYU Biology
output_directory="./$1/biology"
mkdir -p $output_directory
cat "$1-labs-biology" | while read line
do 
	echo "http://biology.as.nyu.edu/object/$line.html" | wget -O- -i- | hxnormalize -x  | hxselect -i p | lynx -stdin -dump -nonumbers -hiddenlinks=ignore > $output_directory/$line
done

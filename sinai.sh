#!/usr/local/bin/bash

#Leaving name as parameter so can combine scraping files later

echo $1
mkdir -p ./${1}
cd $1

<<COMMENT
echo $2 | wget -O- -i- | hxnormalize -x  | hxselect -i ul | lynx -stdin  -dump -nonumbers -hiddenlinks=ignore | grep -i "http" > ${1}-labs
COMMENT

cat ../${1}-labs | while read line
do 
	IFS='/' read -a array<<< $line
	filename="${array[0]##* }"
	echo $line | wget -O- -i- | hxnormalize -x | hxselect -i p | lynx -stdin -dump -nonumbers > $filename
done

<<COMMENT

Will need these two lines for making the combined file, may be easier to do in Python
cat $(ls) > combined 
cat $(ls) | grep  -v "http" | grep -v "file" | grep -v ";" | iconv -f utf-8 -t ascii//translit > cleaned-combined
COMMENT
#!/usr/local/bin/bash

switch=$1
switch=${switch,,}

if [ "$switch" == "nyu" ]
	then 
		echo "Will scrape NYU"
		sh nyu.sh $switch
elif [ "$switch" == "sinai" ] 
	then
		echo "Will scrape Sinai"
		sh sinai.sh $switch
elif [ "$switch" == "rockefeller" ]
	then 
		echo "Will scrape Rockefeller"
		sh rockefeller.sh $switch
else
	echo "University $1 not recognized"
fi 
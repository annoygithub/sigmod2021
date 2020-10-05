#!/bin/bash

cat repo_list | while read star size url
do
	name=`echo $url | awk -F'/' '{print $4"_"$5}'`
	path="repos/${star}_$name"
	echo
	echo "=============git clone $url $path==============="
	git clone $url $path
	rm -r $path/.git
done

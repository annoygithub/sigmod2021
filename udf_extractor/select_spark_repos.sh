#!/bin/sh

for repo in repos/*
do
	l=`grep -r SparkSession $repo | head -n1 | wc -l`
	if [ $l -eq 1 ]
	then
		echo mv $repo spark_$repo
		mv $repo spark_$repo
	fi
done

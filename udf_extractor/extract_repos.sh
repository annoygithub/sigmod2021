for repo in $1/*
do
	mkdir -p udf/$repo/
	echo "-----------------------------------------------------------------------"
	echo "bash extract.sh $repo `pwd`/udf/$repo"
	bash extract.sh $repo `pwd`/udf/$repo 2>&1 | tee udf/$repo/log | grep '^parsed'
	echo
done

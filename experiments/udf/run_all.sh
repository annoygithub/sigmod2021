for i in $@
do
	pushd $i
	echo $i
	python all.py 2>&1 | tee all.log
	popd
done

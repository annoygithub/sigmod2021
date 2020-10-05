for i in */{?,??}.py; 
do
	echo $i; 
	pushd `dirname $i`; 
	name=`basename -s .py $i`; 
	python $name.py &> $name.log;
	popd;
done

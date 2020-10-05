#!/bin/bash

src_path=$1
output_dir=$2

coursier_cache="/home/gzhang9/.cache/coursier/v1/https/repo1.maven.org/maven2"
jar=`pwd`/ast_parser/target/scala-2.11/ast_parser-assembly-0.1.0-SNAPSHOT.jar
spark_cp=$(echo /home/gzhang9/spark-2.4.0-bin-hadoop2.7/jars/spark-* | tr ' ' ':')
log4j_cp="$(echo $coursier_cache/org/apache/logging/log4j/*/2.11.2/*.jar | tr ' ' ':')"
lang3_cp="$(echo $coursier_cache/org/apache/commons/commons-lang3/3.4/*.jar | tr ' ' ':')"
hadoop_cp="$(echo $coursier_cache/org/apache/hadoop/hadoop-hdfs/3.2.1/*.jar | tr ' ' ':')"
hadoop_cp=$hadoop_cp:"$(echo $coursier_cache/org/apache/hadoop/hadoop-core/1.2.1/*.jar | tr ' ' ':')"

scala_cp="/usr/share/scala-2.11/lib/hawtjni-runtime.jar"
scala_cp="$scala_cp:/usr/share/scala-2.11/lib/jansi.jar"
scala_cp="$scala_cp:/usr/share/scala-2.11/lib/jline.jar"
scala_cp="$scala_cp:/usr/share/scala-2.11/lib/scala-actors.jar"
scala_cp="$scala_cp:/usr/share/scala-2.11/lib/scala-compiler.jar"
scala_cp="$scala_cp:/usr/share/scala-2.11/lib/scala-library.jar"
scala_cp="$scala_cp:/usr/share/scala-2.11/lib/scala-parser-combinators.jar"
scala_cp="$scala_cp:/usr/share/scala-2.11/lib/scala-xml.jar"
scala_cp="$scala_cp:/usr/share/scala-2.11/lib/scalap.jar"

pushd $src_path
for src in `find . -name '*.scala'`
do
    dotted_src="${src//\//.}"
    udf_dir="$output_dir/$dotted_src/udf"
    unknown_dir="$output_dir/$dotted_src/unknown"
    excluded_dir="$output_dir/$dotted_src/excluded"
    tmp_dir="$output_dir/$dotted_src/tmp"

    mkdir -p "${udf_dir}" "${unknown_dir}" "${excluded_dir}" "${tmp_dir}"

    # break
    java -cp $jar ast_parser.Breaker $src > $tmp_dir/broken

    # typer
    #echo "scalac -classpath "$spark_cp:$log4j_cp:$lang3_cp:$hadoop_cp"  -sourcepath "$src_path" -Xprint:4  $tmp_dir/broken"
    #scalac -classpath "$spark_cp:$log4j_cp:$lang3_cp:$hadoop_cp"  -sourcepath "$src_path" -Xprint:4  $tmp_dir/broken > $tmp_dir/typed
    java -cp $jar:$scala_cp:$spark_cp:$log4j_cp:$lang3_cp:$hadoop_cp \
         -Dscala.home=/usr/share/scala-2.11 -Dscala.usejavacp=true -Denv.emacs= \
         scala.tools.nsc.interactive.mine.REPL \
         -sourcepath "$src_path" \
         -Ypresentation-any-thread \
         $tmp_dir/broken > $tmp_dir/typed
    
    # get type
    grep -o 'val _t_m_p_[0-9]*: [^=]*' $tmp_dir/typed | grep -o '_t_m_p_[0-9]*: [^=]*' | uniq > $tmp_dir/types

    java -cp $jar ast_parser.Extractor $tmp_dir/broken $tmp_dir/types $udf_dir $unknown_dir $excluded_dir
    # echo "$spark_cp:$log4j_cp:$lang3_cp:$hadoop_cp"
    echo "parsed $src"
done
popd

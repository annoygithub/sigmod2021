#!/bin/bash

JBMC="$HOME/cbmc512/jbmc/src/jbmc/jbmc"
SCAFFOLD_JAR="`pwd`/../product/target/scala-2.11/product_2.11-0.1.0-SNAPSHOT.jar"
JAVA_MODELS="$HOME/cbmc512/jbmc/lib/java-models-library/target/core-models.jar"
NUM_INITIAL_EXAMPLES=5

set -x

rm -fr cegis
mkdir cegis
cd cegis

# generate initial examples
echo "Generating initial examples"
python3 ../product.py > product.scala
scalac product.scala -cp $SCAFFOLD_JAR
scala -cp .:$SCAFFOLD_JAR cegis.product.Product gen $NUM_INITIAL_EXAMPLES > examples

# while true
# do
    # synthesize sql
    echo "Synthesizing sql"
    python3 ../synthesizer.py --ex examples -o sql III

    # generate product program
    echo "Generating the product program"
    python3 ../product.py sql > product.scala
    scalac product.scala -cp $SCAFFOLD_JAR

    # bounded check
    echo "Verifying the product program using jbmc"
    $JBMC cegis.product.Product \
        --classpath .:$JAVA_MODELS:$SCAFFOLD_JAR \
        --function 'cegis.product.Product.product' \
        --java-assume-inputs-non-null --stack-trace --json-ui > jbmc.json

    # add counterexample
    ce=`python3 ../jbmc.py jbmc.json`
    if [ -z "$ce" ]
    then
        echo "No counterexample found. We are done!!! (or something unexpected happened)"
        exit 
    fi
    
    echo "Found new counter example: $ce"
    scala -cp .:$SCAFFOLD_JAR cegis.product.Product run $ce >> examples
# done

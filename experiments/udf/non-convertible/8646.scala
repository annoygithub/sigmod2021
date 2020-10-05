// https://github.com/CODAIT/aardpfark/blob/master//src/test/scala/com/ibm/aardpfark/spark/ml/classification/NaiveBayesSuite.scala
def udf(p: Double, raw: Vector, pr: Vector) = {
    (p, raw.toArray, pr.toArray)
}

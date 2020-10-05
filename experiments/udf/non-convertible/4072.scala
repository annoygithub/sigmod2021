// https://github.com/Syrux/MasterThesis/blob/master//spark/mllib/src/main/scala/org/apache/spark/ml/feature/LSH.scala
def udf(x: Seq[Vector]) = {
     hashDistance(x, keyHash)
}

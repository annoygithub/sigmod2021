// https://github.com/ollik1/spark-clipboard/blob/master//src/main/scala/com/github/ollik1/clipboard/SparkShowRelation.scala
def udf(line: String)  = {
     line.trim.stripPrefix("|").stripSuffix("|")
}

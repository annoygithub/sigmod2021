// https://github.com/zhoulu312/mlengine/blob/master//mlengine-spark/src/test/scala/com/lz/mlengine/spark/ModelTestBase.scala
def udf(x: Row) = {
    val s = x.getAs("value")
     val jsonString = scala.util.parsing.json.JSON.parseFull(s)
    if (jsonString == None)
      false
    else
      true
}

// https://github.com/apache/incubator-s2graph/blob/master//s2jobs/src/main/scala/org/apache/s2graph/s2jobs/udfs/Grok.scala
def udf(text:String): Option[Map[String, String]] = {
    f(text)
}

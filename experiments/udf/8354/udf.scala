// https://github.com/steklopod/Spark-examples/blob/master//src/main/scala/sql/UDF.scala
  def udf(state: String)  = {
    Seq("CA", "OR", "WA", "AK").contains(state)
  }

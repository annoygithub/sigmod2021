// https://github.com/steklopod/Spark-examples/blob/master//src/main/scala/dataframe/UDF.scala
  def udf(thestruct: Row, state: String, discount: Double)  = {
    state == thestruct.getString(0) && discount > thestruct.getDouble(1)
  }

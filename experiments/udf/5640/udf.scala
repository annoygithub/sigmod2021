// https://github.com/bartosz25/spark-scala-playground/blob/master//src/test/scala/com/waitingforcode/sql/RegressionTestsExampleTest.scala
  def udf(row: Row)  = {
     row.getAs[Long]("id") != null && row.getAs[Long]("generated_id") != null
  }


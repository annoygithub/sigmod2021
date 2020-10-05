// https://github.com/bartosz25/spark-scala-playground/blob/master//src/test/scala/com/waitingforcode/sql/extraoptimizations/UnionAdvancedHintTest.scala
  def udf(row: Row)  = {
    s"${row.getAs[String]("letter")}-${row.getAs[Int]("nr")}-${row.getAs[Int]("a_flag")}"
  }


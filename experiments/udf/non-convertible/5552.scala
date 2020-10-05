// https://github.com/bartosz25/spark-scala-playground/blob/master//src/main/scala/com/waitingforcode/structuredstreaming/corrupted_records/IgnoreErrorsLogging.scala
def udf(row: Row) = {
      val convertedLetter = row.getAs[Row]("letter")
      if (convertedLetter == null) {
        println(s"Record ${row.getAs[String]("value_as_string")} cannot be converted")
        false
      } else {
        true
      }
    }

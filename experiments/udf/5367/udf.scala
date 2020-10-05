// https://github.com/romantic123/spark_add_window_function/blob/master//spark-2.0.2/examples/src/main/scala/org/apache/spark/examples/ml/ALSExample.scala
  case class Rating(userId: Int, movieId: Int, rating: Float, timestamp: Long)
  def parseRating(str: String): Rating = {
    val fields = str.split("::")
    Rating(fields(0).toInt, fields(1).toInt, fields(2).toFloat, fields(3).toLong)
  }


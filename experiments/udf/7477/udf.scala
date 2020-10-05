// https://github.com/3cgg/rec-assemble/blob/master//spark/src/main/scala/scala/me/libme/recsystem/ml/FileRatingDataset.scala
case class Rating(userId: Int, movieId: Int, rating: Float, timestamp: Long)
  def parseRating(str: String): Rating = {
    val fields = str.split("::")
    assert(fields.size == 4)
    Rating(fields(0).toInt, fields(1).toInt, fields(2).toFloat, fields(3).toLong)
  }

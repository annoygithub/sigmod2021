// https://github.com/GlassyWing/components-recommend/blob/master//src/test/scala/others/ALSRecommendNewTest.scala
  case class MVRating(userId: Int, movieId: Int, rating: Float, timestamp: Long)
  def parseRating(str: String): MVRating = {
    val fields = str.split("[\t ]+")
    assert(fields.length == 4)
    MVRating(fields(0).toInt, fields(1).toInt, fields(2).toFloat, fields(3).toLong)
  }

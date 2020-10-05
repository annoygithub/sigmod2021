// https://github.com/LevelUpEducation/spark-streaming-scala/blob/master//src/main/scala/StructuredStreaming/solutions/WindowOperationBonusSolution.scala
		case class TweetData(id: BigInt, userName: String, place: String, replyToScreenName: String,
		                     createdAt: String, textLength: BigInt, firstHashtag: String)
  def udf(r: TweetData)  = {
      r.createdAt != null && r.createdAt != "null"
  }

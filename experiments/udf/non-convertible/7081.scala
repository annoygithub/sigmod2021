// https://github.com/aastha0304/KafkaSparkTwitter/blob/master//spark-kafka-sql/src/main/scala/kafkasparksql/KafkaSparkSql.scala
  def sentiment(s:String) : String = {
    val positive = Array("like", "love", "good", "great", "happy", "cool", "the", "one", "that")
    val negative = Array("hate", "bad", "stupid", "is")
    var st = 0;
    val words = s.split(" ")
    positive.foreach(p =>
      words.foreach(w =>
        if(p==w) st = st+1
      )
    )

    negative.foreach(p=>
      words.foreach(w=>
        if(p==w) st = st-1
      )
    )
    if(st>0)
      "positive"
    else if(st<0)
      "negative"
    else
      "neutral"
  }

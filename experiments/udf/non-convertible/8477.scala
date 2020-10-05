// https://github.com/ZhiYinZhang/sparkStudy/blob/master//structuredStreaming/src/main/scala/continous/readKafka.scala
def udf(x: (String, java.sql.Timestamp)) = {
        val str: String = x._1.split("\t")(0)
        val delayMs = x._2.getTime() - Timestamp.valueOf(str).getTime()
        writeToFile(delayMs.toString, resultDataPath)
        val tuple: (String, Timestamp, Timestamp, Long) = (x._1, x._2, new Timestamp(System.currentTimeMillis()), delayMs)
        tuple
      }

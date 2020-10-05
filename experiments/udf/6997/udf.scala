// https://github.com/zhang3550545/structuredstreamngdemo/blob/master//src/main/scala/com/test/KafkaFormat.scala
  def udf(line: (String, String))  = {
      val columns = line._2.split(",")
        (columns(0), columns(1), columns(2))
  }

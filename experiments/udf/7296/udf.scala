// https://github.com/pengzhaopeng/SparkClusterTest/blob/master//src/main/scala/cn/pengzhaopeng/spark/SparkSQL/join/JoinTest.scala
  def udf(line: String)  = {
        val fields: Array[String] = line.split(",")
        val id: String = fields(0)
        val name: String = fields(1)
        val nationCode: String = fields(2)
        (id, name, nationCode)
  }

// https://github.com/ZhangJin1988/spark-sql/blob/master//src/main/scala/cn/zhangjin/spark/day02/IPLocationUDF.scala
def udf(t: String) = {
        val split = t.split("\\|")
        (split(2).toLong, split(3).toLong, split(6))
      }

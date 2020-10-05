// https://github.com/apache/bahir/blob/master//sql-cloudant/examples/src/main/scala/org/apache/spark/examples/sql/cloudant/CloudantApp.scala
  def udf(t: Row)  = {
    "code: " + t(0) + ",name:" + t(1)
  }

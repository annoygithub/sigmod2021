// https://github.com/haichao-zhao/sparksql-train/blob/master//src/main/scala/com/zhc/bigdata/chapter05/DataSourseApp.scala
def udf(x: Row) = {
     x(0) + "|" + x(1).toString
}

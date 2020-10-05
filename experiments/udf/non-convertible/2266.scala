// https://github.com/LinMingQiang/spark-learn/tree/branch-2.4.0/spark-sql/src/main/scala/com/spark/learn/UDFATest.scala
def udf(r: Row) = {
    Row.merge(r, Row("hello"))
}

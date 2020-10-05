// https://github.com/mengzhongtian/spark2.2-maven/blob/master//SparkRepoExample/src/main/scala/org/apache/spark/examples/sql/SparkSQLExample.scala
def udf(teenager: Row) = {
    teenager.getValuesMap[Any](List("name", "age"))
}

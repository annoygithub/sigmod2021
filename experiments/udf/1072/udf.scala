// https://github.com/aydare/datasciencecoursera/blob/master//spark-2.3.1/examples/src/main/scala/org/apache/spark/examples/sql/hive/SparkHiveExample.scala
def udf(key: Int, value: String) = {
    s"Key: $key, Value: $value"
}

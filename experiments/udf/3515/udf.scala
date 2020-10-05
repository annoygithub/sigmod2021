// https://github.com/mengzhongtian/spark2.2-maven/blob/master//SparkRepoExample/examples-scala/sql/hive/SparkHiveExample.scala
def udf(key: Int, value: String) = {
    s"Key: $key, Value: $value"
}

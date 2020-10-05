// https://github.com/gao634209276/mySpark2/blob/master//src/main/scala/example/SparkHiveExample.scala
def udf(key: Int, value: String)  = {
        s"Key: $key, Value: $value"
}

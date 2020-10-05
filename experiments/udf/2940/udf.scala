// https://github.com/yerias/tunan-spark/blob/master//tunan-spark-sql/src/main/scala/com/tunan/spark/sql/udf/StringLength.scala
def udf(love: String) = {
     love.split(",").length
}

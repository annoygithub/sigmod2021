// https://github.com/msjbear/jdata-spark/blob/master//src/main/scala/com/sjmei/jdata/xgboost/SparkModelStackingMain.scala
def udf(row: Row) = {
    (row.get(0).asInstanceOf[String], row.get(1).asInstanceOf[String], row.get(2).asInstanceOf[Int], row.get(3).asInstanceOf[DenseVector].toArray(1), row.get(4).asInstanceOf[Double])
}

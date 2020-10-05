// https://github.com/lz63/spark-learning/blob/master//src/main/scala/com/erongda/bigdata/meituan/product/AreaTop10ProductSparkV2.scala
def udf(id: Int, name: String)  = {
        s"$id:$name"
}

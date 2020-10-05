// https://github.com/xiaomengxun/sparkDemo/blob/master//spark/meituan/product/AreaTop10ProductSparkV3.scala
def udf(id: Int, name: String) = {
     s"$id:$name"
}

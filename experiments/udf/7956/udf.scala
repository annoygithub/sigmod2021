// https://github.com/JimmyCai/xiaomi-dmc-risk-contest/blob/master//src/main/scala/com/xiaomi/miui/ad/statistics/MinMaxStatistics.scala
case class MinMax(min: Double, max: Double)
  def udf(line: String) = {
        val splits = line.split("\t")
        splits.head.toInt -> MinMax(splits(1).toDouble, splits(2).toDouble)
  }

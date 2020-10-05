// https://github.com/JimmyCai/xiaomi-dmc-risk-contest/blob/master//src/main/scala/com/xiaomi/miui/ad/feature_engineering/LightGBMFeature.scala
case class UALProcessed(user: String, time: String, actions: scala.collection.Map[String, scala.collection.Map[Int, Double]], label: Int)
  def udf(ual: UALProcessed, value: Set[String]) = {
        !value.contains(ual.user)
  }

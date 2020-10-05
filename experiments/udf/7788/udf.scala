// https://github.com/996739940/online-education/blob/master//education-etl/src/main/scala/com/atguigu/service/AdlMemberService.scala
  def udf(item: (String, Int)) = {
        val keys = item._1.split("_")
        val adname = keys(0)
        val website = keys(1)
        (adname, item._2, website)
  }

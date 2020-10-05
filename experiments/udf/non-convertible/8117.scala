// https://github.com/SmorSmor/Release/blob/master//src/main/scala/com/release/util/SparkHelper.scala
  def getAgeRange(age: String): String = {
    var tseg = ""
    if (null != age) {
      try {
        tseg = CommonUtil.getAgeRange(age)
      } catch {
        case ex: Exception => {
          println(s"$ex")
        }
      }
    }
    tseg
  }

// https://github.com/cloudframeworks-smack/user-guide-smack/blob/master//source/src/main/scala/com/smack/spark/rpc/service/RankDataService.scala
  def udf(x: Row)  = {
x.getValuesMap[Any](List("totalnum", "totaltime", "maxtime", "mintime"))
  }

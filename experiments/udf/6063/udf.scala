// https://github.com/atgenomix/connectedreads/blob/master//src/main/scala/com/atgenomix/connectedreads/core/rdd/Fragments.scala
  def udf(x: (Long, (Long, String)))  = {
     val a = (x._2._1, x._2._2).swap
     (a._1, a._2)
  }

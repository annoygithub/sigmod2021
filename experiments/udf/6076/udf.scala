// https://github.com/atgenomix/connectedreads/blob/master//src/main/scala/com/atgenomix/connectedreads/core/util/AssembleUtils.scala
  case class Pair(inLabel: Byte, outLabel: Byte,
                  in: (Long, Long), out: (Long, Long),
                  len1: Int, jointLen: Int, len2: Int,
                  startId: Long,
                  endId: Long,
                  overlapLen1: Int, overlapLen2: Int,
                  trigger: Boolean,
                  multi: Boolean)
  def udf(x: Pair)  = {
     (x.in._1, x.in._2) == (-1, -1)
  }

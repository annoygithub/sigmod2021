// https://github.com/atgenomix/connectedreads/blob/master//src/main/scala/com/atgenomix/connectedreads/core/util/GraphUtils.scala
  case class ReadTriplet(reads1: Seq[Long], id1: Long, len1: Int, label1: Byte,
                         overlapLen1: Int,
                         jointReads: Seq[Long], jointId: Long, jointLen: Int,
                         overlapLen2: Int,
                         reads2: Seq[Long],id2: Long, len2: Int, label2: Byte)
  def udf(p: ReadTriplet)  = {
     p.label1 != 0x6 || p.label2 != 0x6
  }

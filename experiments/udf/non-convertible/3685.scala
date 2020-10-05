// https://github.com/josemarialuna/ClusterIndices/blob/master//src/main/scala/es/us/cluster/MainTestLinkage.scala
def udf(r: Row) = {
    r.toSeq.asInstanceOf[Seq[Double]]
}

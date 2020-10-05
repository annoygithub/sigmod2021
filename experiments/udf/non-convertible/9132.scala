// https://github.com/sryza/aas/blob/master//ch07-graph/src/main/scala/com/cloudera/datascience/graph/RunGraph.scala
def udf(topic: String) = {
     val bytes = MessageDigest.getInstance("MD5").digest(str.getBytes(StandardCharsets.UTF_8))
    val hashId = (bytes(0) & 0xFFL) |
    ((bytes(1) & 0xFFL) << 8) |
    ((bytes(2) & 0xFFL) << 16) |
    ((bytes(3) & 0xFFL) << 24) |
    ((bytes(4) & 0xFFL) << 32) |
    ((bytes(5) & 0xFFL) << 40) |
    ((bytes(6) & 0xFFL) << 48) |
    ((bytes(7) & 0xFFL) << 56)
    (hashId, topic)
}

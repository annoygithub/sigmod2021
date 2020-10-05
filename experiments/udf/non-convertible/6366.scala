// https://github.com/PacktPublishing/Hands-On-Big-Data-Analysis-with-Hadoop-3/blob/master//section_2/apache-spark-2-scala-starter-template/src/main/scala/com/tomekl007/anomalydetection/RunKMeans.scala
def udf(x: int, vec: org.apache.spark.ml.linalg.Vector) = {
    Vectors.sqdist(centroids(cluster), vec)
}

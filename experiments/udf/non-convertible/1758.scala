// https://github.com/PacktPublishing/Big-Data-Analytics-Projects-with-Apache-Spark/blob/master//src/main/scala/com/tomekl007/anomalydetection/RunKMeans.scala
def udf(cluster: Int, vec: org.apache.spark.ml.linalg.Vector) = {
    Vectors.sqdist(centroids(cluster), vec)
}

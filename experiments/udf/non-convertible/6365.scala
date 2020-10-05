// https://github.com/PacktPublishing/Hands-On-Big-Data-Analysis-with-Hadoop-3/blob/master//section_2/apache-spark-2-scala-starter-template/src/main/scala/com/tomekl007/anomalydetection/RunKMeans.scala
def udf(row: Row) = { 
        val cluster = row.getAs[Int]("cluster")
        val vec = row.getAs[Vector]("scaledFeatureVector")
        Vectors.sqdist(centroids(cluster), vec) >= farthestDistanceBetweenTwoNormalClusters
      }

// https://github.com/dmarcous/dDBGSCAN/blob/master//src/main/scala/com/github/dmarcous/ddbgscan/core/preprocessing/GeoPropertiesExtractor.scala
def udf(id: Long, lon: Long, lat: Long, features: org.apache.spark.ml.linalg.Vector)) = {
    (new KeyGeoEntity(LonLatGeoEntity(lon, lat), neighborhoodPartitioningLvl), new ClusteringInstance(recordId = id, lonLatLocation = (lon, lat), features = features))
}

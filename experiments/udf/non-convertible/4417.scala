// https://github.com/zhoulu312/mlengine/blob/master//mlengine-spark/src/test/scala/com/lz/mlengine/spark/ModelTestBase.scala
def udf(row: com.lz.mlengine.spark.SVMData) = {
    new TestProbabilityVector(row.id, model.predictImpl(row.features))
}

// https://github.com/databricks/spark-sql-perf/blob/master//src/main/scala/com/databricks/spark/sql/perf/DatasetPerformance.scala
case class Data(id: Long)
  def udf(data: Data)  = {
    data.id % 103 != 0
  }

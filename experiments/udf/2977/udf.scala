// https://github.com/zixuedanxin/bigdata_learn/blob/master//spark-scala-learn/src/main/scala/com/bigdata/sql/n_03_spark_dataframe/n_24_dataframe_sql_map_fieldName/Run.scala
def udf(people: Row) = {
     "name:" + people.getAs[String]("name") + "\tage:" + people.getAs[Long]("age")
}

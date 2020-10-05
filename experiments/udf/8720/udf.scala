// https://github.com/bastihaase/Insight18b-SparkSQL-Array/blob/master//sparksql_performance_tests/src/main/scala/Performance_Tests/SparkSQL_Performance_Group_By_Size.scala
  def udf(arr1: Seq[String], arr2: Seq[String])  = {
    if (arr1 != null && arr2 != null)
        arr1.intersect(arr2)
    else
        Seq[String]()
  }

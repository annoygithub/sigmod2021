// https://github.com/David082/SparkML/blob/master//src/main/scala/hotel/features/SparkSim.scala
def udf(row: Row) = {
    val merge = SimSql.mergeCol(row, 9, userPriceFreq.length)
        (row(0).toString, row(1).toString, row(2).toString, row(3).toString.toInt, row(4).toString.toInt, row(5).toString, row(6).toString, row(7).toString.toInt, row(8).toString.toDouble, merge.toArray)
      }


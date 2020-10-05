// https://github.com/bartosz25/spark-scala-playground/blob/master//src/test/scala/com/waitingforcode/sql/JoinTypesTest.scala
  def mapJoinedRow(row: Row): String = {
    val orderId = if (row.isNullAt(0)) null else row.getInt(0)
    val orderCustomerId = if (row.isNullAt(1)) null else row.getInt(1)
    val orderAmount = if (row.isNullAt(2)) null else row.getDouble(2)
    val customerId = if (row.isNullAt(3)) null else row.getInt(3)
    val customerName = if (row.isNullAt(4)) null else row.getString(4)
    s"${orderId},${orderCustomerId},${orderAmount},${customerId},${customerName}"
  }

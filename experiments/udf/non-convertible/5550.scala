// https://github.com/datastax/spark-cassandra-stress/blob/master//src/main/scala/com/datastax/sparkstress/WriteTask.scala
def udf(row: Row) = {
    row.toString()
}

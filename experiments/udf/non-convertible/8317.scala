// https://github.com/nathan-gs/eventhubs-reingest/blob/master//src/main/scala/gs/nathan/eventhubsreingest/sql/udfs/RandomPartition.scala
def udf() = {
     Random.nextInt(partitionSize + 1)
}

// https://github.com/rajeshvenkatesan/Hbase/blob/master//src/main/scala/com/hbase/write/WriteToHbase.scala
def udf(f: Row) = {
    f.getAs("_unit_id").toString.forall(_.isDigit)
}

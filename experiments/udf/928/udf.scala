// https://github.com/lastbus/recommend/blob/master//src/main/scala/com/bl/bigdata/product/CategoryStatistic.scala
def udf(r: Row) = {
     (if (r.isNullAt(0)) -99 else r.getLong(0), if (r.isNullAt(1)) 0 else r.getLong(1))
}

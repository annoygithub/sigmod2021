// https://github.com/yarson/garbage_classification/blob/master//index/src/main/scala/com/open/data/IndexBuilder.scala
def udf(r: Row) = {
    r.mkString("\t")
}

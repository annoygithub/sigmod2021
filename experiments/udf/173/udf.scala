// https://github.com/Jeffersonmf/zap_sessionization_teste/blob/master//src/main/scala/core/EnrichmentEngine.scala
def udf(result: Row) = {
    result.getValuesMap[Any](List("os_family", "count"))
}


// https://github.com/josemarialuna/ExternalValidity/blob/master//src/main/scala/es/us/spark/mllib/clustering/validation/ExternalValidation.scala
def udf(row: Row) = {
    val variationOfInformationSeq = for (i <- 0 until row.size) yield {
            val cellValue = row.getLong(i)
            combina2(cellValue)
          }
          variationOfInformationSeq.sum
        }

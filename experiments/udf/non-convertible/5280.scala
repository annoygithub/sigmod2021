// https://github.com/monk1337/TransmogrifAI/blob/master//features/src/main/scala/com/salesforce/op/utils/spark/RichDataset.scala
def udf(row: Row) = {
    predicate(row.getAs[T](columnName))
}

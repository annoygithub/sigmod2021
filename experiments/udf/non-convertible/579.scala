// https://github.com/yongsheng268/Spark-NLP/blob/master//eval/src/main/scala/com/johnsnowlabs/nlp/eval/SymSpellEvaluation.scala
def udf(row: Row) = {
    !(row.mkString("").isEmpty && row.length > 0)
}

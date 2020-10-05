// https://github.com/EDS-APHP/UimaOnSpark/blob/master//src/main/scala/fr/aphp/wind/uima/spark/SentenceExtract.scala
def udf(x: fr.aphp.wind.uima.spark.SentenceSegmenter.Text) = {
    tt.analyzeText(x.text).asInstanceOf[String]
}

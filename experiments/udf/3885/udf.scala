// https://github.com/forchard/demy/blob/master//mllib/src/main/scala/text/TermlLikelyhoodEvaluator.scala
def udf(r: Row)  = {
    r.getAs[Double](scoresColumnName) match {
          case 0.0d => -1
          case 1.0d => 1
        }
}

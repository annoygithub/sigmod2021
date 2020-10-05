// https://github.com/FINRAOS/CodeSamples/blob/master//machine-learning-samples/src/main/scala/org/finra/ezmachinelearning/RFWithSurrogateCensusIncomeExample.scala
  def udf(x: Double, y: Double)  = {
     scala.math.pow(x - y, 2)
  }

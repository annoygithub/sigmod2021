// https://github.com/reddy279/SparkMachineLearningRef/blob/master//src/main/scala-2.11/com/emergency/calls/analysis/uc1/EmergencyCallsAnlysis.scala
def udf(x: Row)  = {
     x(0) + " -> " + s"(${x(1)}, ${x(2)})"
}

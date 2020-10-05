// https://github.com/curtishoward/sparkudfexamples/blob/master//scala-udf/src/main/scala/com/cloudera/fce/curtis/sparkudfexamples/scalaudf/ScalaUDFExample.scala
def udf(degreesCelcius: Double)  = {
    degreesCelcius * 9.0d / 5.0d + 32.0d
}

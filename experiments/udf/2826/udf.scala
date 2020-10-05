// https://github.com/stayrascal/rascal-spark/blob/master//rascal-data/src/main/scala/com/stayrascal/spark/example/airplane/AirplaneExample.scala
case class Flight(dayOfMonth: Int, dayOfWeek: Int, crsDepTime: Double, crsArrTime: Double, uniqueCarrier: String,
                  crsElapsedTime: Double, origin: String, dest: String, arrDelay: Int, depDelay: Int, delayFlag: Int)

  def parseFields(input: String): Flight = {
    val line = input.split(",")
    var dayOfMonth = if (line(0) != "NA") line(0).toInt else 0
    var dayOfWeek = if (line(1) != "NA") line(1).toInt else 0
    var crsDepTime = if (line(2) != "NA") line(2).toDouble else 0.0
    var crsArrTime = if (line(3) != "NA") line(3).toDouble else 0.0
    var crsElapsedTime = if (line(5) != "NA") line(5).toDouble else 0.0
    var arrDelay = if (line(8) != "NA") line(8).toInt else 0
    var depDelay = if (line(9) != "NA") line(9).toInt else 0
    var delayFlag = if (arrDelay > 30 || depDelay > 30) 1 else 0
    Flight(dayOfMonth, dayOfWeek, crsDepTime, crsArrTime, line(4), crsElapsedTime, line(6), line(7), arrDelay, depDelay, delayFlag)
  }

// https://github.com/apantea01/CSE511Project/blob/master//CSE512-Project-Hotspot-Analysis-Template-master/src/main/scala/cse512/HotzoneAnalysis.scala
def udf(rectangleData: String, pointData: String): Boolean  = {
    val rectangle_dataStringArray = rectangleData.split(",")

    val rectangle_point1_xInput = rectangle_dataStringArray(0)
    val rectangle_point1_yInput = rectangle_dataStringArray(1)

    val rectangle_point2_xInput = rectangle_dataStringArray(2)
    val rectangle_point2_yInput = rectangle_dataStringArray(3)

    val rectangle_point1_x = rectangle_point1_xInput.trim.toDouble
    val rectangle_point2_x = rectangle_point2_xInput.trim.toDouble
    val rectangle_lowerBound_x = if (rectangle_point1_x < rectangle_point2_x)
      rectangle_point1_x
    else rectangle_point2_x

    val rectangle_point1_x1 = rectangle_point1_xInput.trim.toDouble
    val rectangle_point2_x1 = rectangle_point2_xInput.trim.toDouble
    val rectangle_higherBound_x = if (rectangle_point1_x1 > rectangle_point2_x1)
      rectangle_point1_x1
    else rectangle_point2_x1

    val rectangle_point1_y = rectangle_point1_yInput.trim.toDouble
    val rectangle_point2_y = rectangle_point2_yInput.trim.toDouble
    val rectangle_lowerBound_y = if (rectangle_point1_y < rectangle_point2_y)
      rectangle_point1_y
    else rectangle_point2_y

    val rectangle_point1_y1 = rectangle_point1_yInput.trim.toDouble
    val rectangle_point2_y1 = rectangle_point2_yInput.trim.toDouble
    val rectangle_higherBound_y = if (rectangle_point1_y1 > rectangle_point2_y1)
      rectangle_point1_y1
    else rectangle_point2_y1

    var pointStringArray = pointData.split(",") 
    val point_xInput = pointStringArray(0)
    val point_yInput = pointStringArray(1)

    val point_x = point_xInput.trim.toDouble
    val point_x1 = point_xInput.trim.toDouble
    if (point_x < rectangle_lowerBound_x || point_x1 > rectangle_higherBound_x)
        false
    else {  
      val point_y = point_yInput.trim.toDouble
      val point_y1 = point_yInput.trim.toDouble
      if (point_y > rectangle_lowerBound_y || point_y1 < rectangle_higherBound_y)
        false
      else
        true
    }
  } 

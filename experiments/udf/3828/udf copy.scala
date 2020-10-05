def udf(rectangleData: String, pointData: String): Boolean  = {
    var rectangle_dataStringArray = rectangleData.split(",")
    // cast(trim(substring_index(a, ',', 1)) as int)
    // val c4 = c3.selectExpr("a", "b", "cast(trim(substring_index(a, ',', 1)) as int) as rectangle_point1_x")
    var rectangle_point1_x = rectangle_dataStringArray(0).trim.toDouble
    // cast(trim(substring_index(substring_index(a, ',', 2), ',', -1)) as int)
    // val c5 = c4.selectExpr("a", "b", "rectangle_point1_x", "cast(trim(substring_index(substring_index(a, ',', 2), ',', -1)) as int) as rectangle_point1_y")
    var rectangle_point1_y = rectangle_dataStringArray(1).trim.toDouble
    // cast(trim(substring_index(substring_index(a, ',', 3), ',', -1)) as int)
    // val c6 = c5.selectExpr("a", "b", "rectangle_point1_x", "rectangle_point1_y", "cast(trim(substring_index(substring_index(a, ',', 3), ',', -1)) as int) as rectangle_point2_x")
    var rectangle_point2_x = rectangle_dataStringArray(2).trim.toDouble
    // cast(trim(substring_index(substring_index(a, ',', 4), ',', -1)) as int)
    // val c7 = c6.selectExpr("a", "b", "rectangle_point1_x", "rectangle_point1_y", "rectangle_point2_x", "cast(trim(substring_index(substring_index(a, ',', 4), ',', -1)) as int) as rectangle_point2_y")
    var rectangle_point2_y = rectangle_dataStringArray(3).trim.toDouble
    // if(cast(trim(substring_index(a, ',', 1)) as int) < cast(trim(substring_index(substring_index(a, ',', 3), ',', -1)) as int), cast(trim(substring_index(a, ',', 1)) as int), cast(trim(substring_index(substring_index(a, ',', 3), ',', -1)) as int))
    // val c8 = c7.selectExpr("a", "b", "rectangle_point1_x", "rectangle_point1_y", "rectangle_point2_x", "rectangle_point2_y", "if(rectangle_point1_x < rectangle_point2_x, rectangle_point1_x, rectangle_point2_x) as rectangle_lowerBound_x")
    var rectangle_lowerBound_x = math.min(rectangle_point1_x, rectangle_point2_x)
    // if(cast(trim(substring_index(a, ',', 1)) as int) > cast(trim(substring_index(substring_index(a, ',', 3), ',', -1)) as int), cast(trim(substring_index(a, ',', 1)) as int), cast(trim(substring_index(substring_index(a, ',', 3), ',', -1)) as int))
    // val c9 = c8.selectExpr("a", "b", "rectangle_point1_x", "rectangle_point1_y", "rectangle_point2_x", "rectangle_point2_y", "rectangle_lowerBound_x", "if(rectangle_point1_x > rectangle_point2_x, rectangle_point1_x, rectangle_point2_x) as rectangle_higherBound_x")
    var rectangle_higherBound_x = math.max(rectangle_point1_x, rectangle_point2_x)
    // if(cast(trim(substring_index(substring_index(a, ',', 2), ',', -1)) as int) < cast(trim(substring_index(substring_index(a, ',', 4), ',', -1)) as int), cast(trim(substring_index(substring_index(a, ',', 2), ',', -1)) as int), cast(trim(substring_index(substring_index(a, ',', 4), ',', -1)) as int))
    // val c10 = c9.selectExpr("a", "b", "rectangle_point1_x", "rectangle_point1_y", "rectangle_point2_x", "rectangle_point2_y", "rectangle_lowerBound_x", "rectangle_higherBound_x", "if(rectangle_point1_y < rectangle_point2_y, rectangle_point1_y, rectangle_point2_y) as rectangle_lowerBound_y")
    var rectangle_lowerBound_y = math.min(rectangle_point1_y, rectangle_point2_y)
    // if(cast(trim(substring_index(substring_index(a, ',', 2), ',', -1)) as int) > cast(trim(substring_index(substring_index(a, ',', 4), ',', -1)) as int), cast(trim(substring_index(substring_index(a, ',', 2), ',', -1)) as int), cast(trim(substring_index(substring_index(a, ',', 4), ',', -1)) as int))
    // val c11 = c10.selectExpr("a", "b", "rectangle_point1_x", "rectangle_point1_y", "rectangle_point2_x", "rectangle_point2_y", "rectangle_lowerBound_x", "rectangle_higherBound_x", "rectangle_lowerBound_y", "if(rectangle_point1_y > rectangle_point2_y, rectangle_point1_y, rectangle_point2_y) as rectangle_higherBound_y")
    var rectangle_higherBound_y = math.max(rectangle_point1_y, rectangle_point2_y)
    var pointStringArray: Array[String] = pointData.split(",")  
    // cast(trim(substring_index(b, ',', 1)) as int)
    // val c12 = c11.selectExpr("a", "b", "rectangle_point1_x", "rectangle_point1_y", "rectangle_point2_x", "rectangle_point2_y", "rectangle_lowerBound_x", "rectangle_higherBound_x", "rectangle_lowerBound_y", "rectangle_higherBound_y", "cast(trim(substring_index(b, ',', 1)) as int) as point_x")
    var point_x = pointStringArray(0).trim.toDouble
    // cast(trim(substring_index(substring_index(b, ',', 2), ',', -1)) as int)
    // val c13 = c12.selectExpr("a", "b", "rectangle_point1_x", "rectangle_point1_y", "rectangle_point2_x", "rectangle_point2_y", "rectangle_lowerBound_x", "rectangle_higherBound_x", "rectangle_lowerBound_y", "rectangle_higherBound_y", "point_x", "cast(trim(substring_index(substring_index(b, ',', 2), ',', -1)) as int) as point_y")
    var point_y = pointStringArray(1).trim.toDouble
    // if ((cast(trim(substring_index(b, ',', 1)) as int) < if(cast(trim(substring_index(a, ',', 1)) as int) < cast(trim(substring_index(substring_index(a, ',', 3), ',', -1)) as int), cast(trim(substring_index(a, ',', 1)) as int), cast(trim(substring_index(substring_index(a, ',', 3), ',', -1)) as int)) or (cast(trim(substring_index(b, ',', 1)) as int) > if(cast(trim(substring_index(a, ',', 1)) as int) > cast(trim(substring_index(substring_index(a, ',', 3), ',', -1)) as int), cast(trim(substring_index(a, ',', 1)) as int), cast(trim(substring_index(substring_index(a, ',', 3), ',', -1)) as int)))), false, if((cast(trim(substring_index(substring_index(b, ',', 2), ',', -1)) as int) > if(cast(trim(substring_index(substring_index(a, ',', 2), ',', -1)) as int) > cast(trim(substring_index(substring_index(a, ',', 4), ',', -1)) as int), cast(trim(substring_index(substring_index(a, ',', 2), ',', -1)) as int), cast(trim(substring_index(substring_index(a, ',', 4), ',', -1)) as int))) or (cast(trim(substring_index(substring_index(b, ',', 2), ',', -1)) as int) < if(cast(trim(substring_index(substring_index(a, ',', 2), ',', -1)) as int) < cast(trim(substring_index(substring_index(a, ',', 4), ',', -1)) as int), cast(trim(substring_index(substring_index(a, ',', 2), ',', -1)) as int), cast(trim(substring_index(substring_index(a, ',', 4), ',', -1)) as int))), false, true))
    // 
    if (point_x < rectangle_lowerBound_x || point_x > rectangle_higherBound_x) return false
    if (point_y > rectangle_higherBound_y || point_y < rectangle_lowerBound_y) return false
    return true
  }

if(cast(trim(substring_index(a, ',', 0))

def udf2(a:String, b:String, c:Double, d:Long, e:String, f:String) : Boolean ={
  a == "Brand#23" && 
  (b=="MED CASE" || b == "MED BOX" || b == "MED PACK" || b == "MED PKG") && 
  c >= 10.0 && c <= 10.0+ 10.0 && 
  d>=1 && d<= 10 && 
  (e=="AIR" || e == "AIR REG") && 
  f == "DELIVER IN PERSON"
}

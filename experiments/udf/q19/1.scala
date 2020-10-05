def udf1(a:String, b:String, c:Double, d:Long, e:String, f:String) : Boolean ={
  a == "Brand#12" && 
  (b=="SM CASE" || b == "SM BOX" || b == "SM PACK" || b == "SM PKG") && 
  c >= 1.0 && c <= 1.0+ 10.0 && 
  d>=1 && d<= 5 && 
  (e=="AIR" || e == "AIR REG") && 
  f == "DELIVER IN PERSON"
}

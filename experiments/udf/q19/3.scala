def udf3(a:String, b:String, c:Double, d:Long, e:String, f:String) : Boolean ={
  a == "Brand#34" && 
  (b=="LG CASE" || b == "LG BOX" || b == "LG PACK" || b == "LG PKG") && 
  c >= 20.0 && c <= 20.0 + 10.0 && 
  d>=1 && d<= 15 && 
  (e=="AIR" || e == "AIR REG") && 
  f =="DELIVER IN PERSON"
}

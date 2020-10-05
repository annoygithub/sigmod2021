
def udf2(a: String,b:String,c:Long, d: String, e: String) : Boolean ={
  a != "Brand#45" && 
  (!b.startsWith("MEDIUM POLISHED")) && 
  (c == 49 || c == 14 || c == 23 || c == 45 || c == 19 || c == 3 || c == 36 || c == 9) && 
  (d == e || d != e)
}

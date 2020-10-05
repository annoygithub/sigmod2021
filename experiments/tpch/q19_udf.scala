def udf1(a:String, b:String, c:Double, d:Long, e:String, f:String) : Boolean ={
  a == "Brand#12" && 
  (b=="SM CASE" || b == "SM BOX" || b == "SM PACK" || b == "SM PKG") && 
  c >= 1.0 && c <= 1.0+ 10.0 && 
  d>=1 && d<= 5 && 
  (e=="AIR" || e == "AIR REG") && 
  f == "DELIVER IN PERSON"
}

def udf2(a:String, b:String, c:Double, d:Long, e:String, f:String) : Boolean ={
  a == "Brand#23" && 
  (b=="MED CASE" || b == "MED BOX" || b == "MED PACK" || b == "MED PKG") && 
  c >= 10.0 && c <= 10.0+ 10.0 && 
  d>=1 && d<= 10 && 
  (e=="AIR" || e == "AIR REG") && 
  f == "DELIVER IN PERSON"
}

def udf3(a:String, b:String, c:Double, d:Long, e:String, f:String) : Boolean ={
  a == "Brand#34" && 
  (b=="LG CASE" || b == "LG BOX" || b == "LG PACK" || b == "LG PKG") && 
  c >= 20 && c <= 20+ 10 && 
  d>=1 && d<= 15 && 
  (e=="AIR" || e == "AIR REG") && 
  f =="DELIVER IN PERSON"
}

def udf4(a: Double, b: Double): Double = {
    val v = 1.0 - b
    a * v
}

spark.udf.register("udf1", udf1 _)
spark.udf.register("udf2", udf2 _) 
spark.udf.register("udf3", udf3 _) 
spark.udf.register("udf4", udf4 _) 

val res=spark.sql(
"""
select
        sum(udf4(l_extendedprice, l_discount)) as revenue
from
        lineitem,
        part
where
        (
                p_partkey = l_partkey
                and udf1(p_brand,p_container,l_quantity,p_size,l_shipmode,l_shipinstruct)
        )
        or
        (
                p_partkey = l_partkey
                and udf2(p_brand,p_container,l_quantity,p_size,l_shipmode,l_shipinstruct)
        )
        or
        (
                p_partkey = l_partkey
                and udf3(p_brand,p_container,l_quantity,p_size,l_shipmode,l_shipinstruct)
        )
""")

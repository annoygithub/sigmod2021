def udf1(a: Double, b: Double): Double = {
    a / b
}
def udf2(a: Double, b: Double): Double = {
    a * b
}
def udf3(a: String, b:String, c: Double, d: Double) : Boolean ={
  a == "Brand#23" && 
  b == "MED BOX" &&
  c < d
}


spark.udf.register("udf1", udf1 _)
spark.udf.register("udf2", udf2 _) 
spark.udf.register("udf3", udf3 _) 

val res=spark.sql(
"""
select
         udf1(sum(l_extendedprice), 7.0) as avg_yearly
from
         lineitem,
         part,
         (
                   select
                            l_partkey m_l_partkey,
                            udf2(0.2, avg(l_quantity)) m_avg
                   from
                            lineitem
                   group by
                            l_partkey
         ) v
where
         p_partkey = l_partkey
         and udf3(p_brand,p_container, l_quantity, v.m_avg)
         and p_partkey = v.m_l_partkey
""")


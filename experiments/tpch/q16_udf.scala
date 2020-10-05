def udf1(r_name: String) : Boolean ={
  (r_name.indexOf("Customer") >= 0 &&
    r_name.indexOf("Complaints", r_name.indexOf("Customer")) > 0)
}


def udf2(a: String,b:String,c:Long, d: String, e: String) : Boolean ={
  a != "Brand#45" && 
  (!b.startsWith("MEDIUM POLISHED")) && 
  (c == 49 || c == 14 || c == 23 || c == 45 || c == 19 || c == 3 || c == 36 || c == 9) && 
  (d == e || d != e)
}


spark.udf.register("udf1", udf1 _)
spark.udf.register("udf2", udf2 _) 

val res=spark.sql(
"""
select
         p_type,
         p_size,
         count(distinct ps_suppkey) as supplier_cnt
from
         partsupp,
         part,
         (
                   select
                       s_suppkey m_s_suppkey
                   from
                            supplier
                   where
                            udf1(s_comment)
         ) v
where
         p_partkey = ps_partkey
         and udf2(p_brand,p_type,p_size, ps_suppkey, v.m_s_suppkey)
group by
         p_brand,
         p_type,
         p_size
order by
         supplier_cnt desc,
         p_brand,
         p_type,
         p_size
""")


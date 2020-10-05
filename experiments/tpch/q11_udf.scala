def udf1(a: Double, b: Double) : Double = {
    a*b
}
def udf2(r_name: String) : Boolean ={
    r_name=="GERMANY"
}
def udf3(a: Double, b: Double): Boolean = {
    a > b
}

spark.udf.register("udf1", udf1 _)
spark.udf.register("udf2", udf2 _) 
spark.udf.register("udf3", udf3 _) 

val res=spark.sql(
"""
select
        ps_partkey,
        sum(udf1(ps_supplycost, ps_availqty)) as value
from
        partsupp,
        supplier,
        nation
where
        ps_suppkey = s_suppkey
        and s_nationkey = n_nationkey
        and udf2(n_name)
group by
        ps_partkey having
                udf3(sum(udf1(ps_supplycost, ps_availqty)), (
                        select
                                udf1(sum(udf1(ps_supplycost, ps_availqty)), 0.0001000000)
                        from
                                partsupp,
                                supplier,
                                nation
                        where
                                ps_suppkey = s_suppkey
                                and s_nationkey = n_nationkey
                                and udf2(n_name)
                ))
order by
        value desc
""")

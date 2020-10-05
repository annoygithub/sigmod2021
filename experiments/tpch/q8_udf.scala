def udf1(nation: String, volume: Double): Double = {
    if (nation == "BRAZIL") volume else 0.0
}

def udf2(a: Double, b: Double): Double = {
    a / b
}

def udf3(l_extendedprice: Double,  l_discount: Double) : Double = {
    val v1 = 1.0 - l_discount
    l_extendedprice * v1
}

def udf4(a:String, b: String) : Boolean ={
    a == "AMERICA" && b == "ECONOMY ANODIZED STEEL"
}

spark.udf.register("udf1", udf1 _)
spark.udf.register("udf2", udf2 _)
spark.udf.register("udf3", udf3 _)
spark.udf.register("udf4", udf4 _)

val res=spark.sql(
"""
select
        o_year,
        udf2(sum(udf1(nation, volume)), sum(volume)) as mkt_share
from
        (
                select
                        year(o_orderdate) as o_year,
                        udf3(l_extendedprice, l_discount) as volume,
                        n2.n_name as nation
                from
                        part,
                        supplier,
                        lineitem,
                        orders,
                        customer,
                        nation n1,
                        nation n2,
                        region
                where
                        p_partkey = l_partkey
                        and s_suppkey = l_suppkey
                        and l_orderkey = o_orderkey
                        and o_custkey = c_custkey
                        and c_nationkey = n1.n_nationkey
                        and n1.n_regionkey = r_regionkey
                        and udf4(r_name, p_type)
                        and s_nationkey = n2.n_nationkey
                        and o_orderdate between date '1995-01-01' and date '1996-12-31'
        ) as all_nations
group by
        o_year
order by
        o_year
""")

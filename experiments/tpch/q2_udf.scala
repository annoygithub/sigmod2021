def udf1(p_size: Long, r_name: String, p_type: String) : Boolean ={
    r_name=="EUROPE" && p_size==15 && (p_type.substring(p_type.length-5, p_type.length) == "BRASS")
}
def udf2(r_name: String) : Boolean ={
    r_name=="EUROPE"
}

spark.udf.register("udf1", udf1 _)
spark.udf.register("udf2", udf2 _)

val res=spark.sql(
     """
     select
     s_acctbal,
     s_name,
     n_name,
     p_partkey,
     p_mfgr,
     s_address,
     s_phone,
     s_comment
 from
     part,
     supplier,
     partsupp,
     nation,
     region,
     (select
                             min(ps_supplycost) v_ps_supplycost,
                             ps_partkey v_ps_partkey
                    from
                             partsupp t1,
                             supplier t2,
                             nation t3,
                             region t4
                    where
                             t2.s_suppkey = t1.ps_suppkey
                             and t2.s_nationkey = t3.n_nationkey
                             and t3.n_regionkey = t4.r_regionkey
                             and udf2(t4.r_name)
                    group by
                             ps_partkey) v
 where
     p_partkey = ps_partkey
     and s_suppkey = ps_suppkey
     and udf1(p_size,r_name, p_type)
     and s_nationkey = n_nationkey
     and n_regionkey = r_regionkey
     and ps_supplycost = v.v_ps_supplycost
      and p_partkey = v.v_ps_partkey
 order by
     s_acctbal desc,
     n_name,
     s_name,
     p_partkey
     """)

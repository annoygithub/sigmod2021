def udf1(p_size: Long, r_name: String, p_type: String) : Boolean ={
    r_name=="EUROPE" && p_size==15 && (p_type.substring(p_type.length-5, p_type.length) == "BRASS")
}

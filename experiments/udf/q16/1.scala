def udf1(r_name: String) : Boolean ={
  (r_name.indexOf("Customer") >= 0 &&
    r_name.indexOf("Complaints", r_name.indexOf("Customer")) > 0)
}

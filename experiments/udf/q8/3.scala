
def udf3(l_extendedprice: Double,  l_discount: Double) : Double = {
    val v1 = 1.0 - l_discount
    l_extendedprice * v1
}

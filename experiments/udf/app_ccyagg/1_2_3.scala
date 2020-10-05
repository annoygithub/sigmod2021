case class CCYTrade(category: String, customerId: Int, localDate: String, x: String, y: String, z: String, percent: Int)
def udf(r: String) = {
    val fields = r.split(",").map(_.trim)
    CCYTrade(fields(0), fields(1).toInt, fields(2), fields(3), fields(4), fields(5), fields(6).toInt)
}

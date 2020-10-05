case class CCYTrade(category: String, customerId: Int, localDate: String, x: String, y: String, z: String, percent: Int)
def udf(x: CCYTrade) = {
    x.percent
}

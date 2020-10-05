// https://github.com/geerdink/fast-data/blob/master//lambda/src/main/scala/etl/BatchEtl.scala
case class Customer (id: Int, name: String, age: Int, title: String, street: String, number: Int, postCode: String, email: String, premium: Boolean)
case class Product (name: String, url: String, price: Double)
case class Order (id: Int, customer: Customer, product: Product, amount: Int)


def udf(r: (Customer, Order), total: Double)  = {
    s"${r._1.name} has ordered ${r._2.amount} units of ${r._2.product.name}s, for a total price of $total"
}

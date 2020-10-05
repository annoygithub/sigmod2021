// https://github.com/HPI-Information-Systems/spark-tutorial/blob/master//src/main/scala/de/hpi/spark_tutorial/SimpleSpark.scala
case class Pet(name:String, age:Int)

def udf(x: Pet)  = {
        val name = x.name
        val age = x.age
        s"Pet(name=${name}, age=${age})" + " is cute"
}

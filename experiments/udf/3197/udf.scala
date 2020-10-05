// https://github.com/sparkbyexamples/spark-examples/blob/master//spark-sql-examples/src/main/scala/com/sparkbyexamples/spark/stackoverflow/AddingLiterral.scala
case class EmpData(key: String,value:String)
case class Employee(EmpId: String, Experience: Double, Salary: Double)
def udf(rec: Employee) = {
     (EmpData("1", rec.EmpId), EmpData("2", rec.Experience.toString), EmpData("3", rec.Salary.toString))
}

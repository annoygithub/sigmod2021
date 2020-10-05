package cegis.product

import java.lang.reflect.Method
import scala.util.{Random => R}

object ExampleGenerator {
    def genInt() = R.nextInt(1<<15)

    def hex(str: String) = str.map(_.toInt.toHexString).mkString

    def unhex(str: String) = str.sliding(2, 2).toArray.map(Integer.parseInt(_, 16).toChar).mkString

    def toJson(v: Any) = v match {
        case v : Int => s"$v"
        case v : String => s""""${hex(v)}""""
        case v : Boolean => s"${if (v) "true" else "false"}"
    }

    def parseInput(method: Method, input: Array[String]) = {
       method.getParameterTypes().zip(input).map({case (tpe, str) => tpe match {
           case q if q == classOf[Int] => str.toInt.asInstanceOf[AnyRef]
           case q if q == classOf[String] => unhex(str.drop(1).dropRight(1))
           case q if q == classOf[Boolean] => (if (q == "true") true else false).asInstanceOf[AnyRef]
       }})
    }

    def genString() = {
        val abc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        val n = R.nextInt(10)
        (0 to n).map(_ => abc(R.nextInt.abs % abc.size)).mkString
    }

    def genBoolean() = R.nextBoolean()

    def genInput(method: Method) = {
        method.getParameterTypes().map(tpe => tpe match {
            case q if q == classOf[Int] => genInt.asInstanceOf[AnyRef]
            case q if q == classOf[String] => genString()
            case q if q == classOf[Boolean] => genBoolean().asInstanceOf[AnyRef]
        })
    }

    def runInput(method: Method, ob: AnyRef, input: Array[AnyRef]): String = {
        val output = method.invoke(ob, input: _*)
        s"""{"input": [${input.map(toJson(_)).mkString(", ")}], "output": ${toJson(output)}}"""
    }

    def genExample(method: Method, ob: AnyRef) = 
        runInput(method, ob, genInput(method))

    def runInput(method: Method, ob: AnyRef, input: Array[String]): Unit = 
        println(runInput(method, ob, parseInput(method, input)))

    def runInput(methodName: String, ob: AnyRef, input: Array[String]): Unit = {
        val method = ob.getClass().getDeclaredMethods().filter(_.getName() == methodName)(0);
        runInput(method, ob, input)
    }

    def genExamples(method: Method, ob: AnyRef, count: Int): Unit = 
        0 until count foreach(_ => try{
            println(genExample(method, ob))
        }
        catch{
            case x: Throwable => Console.err.println(s"Exception: $x")
        })

    // for non-static function
    def genExamples(methodName: String, ob: AnyRef, count: Int): Unit = {
        val method = ob.getClass().getDeclaredMethods().filter(_.getName() == methodName)(0);
        genExamples(method, ob, count)
    }

    // for static function
    def genExamples(klass: Class[_], methodName: String, count: Int): Unit = {
        val method = klass.getDeclaredMethods().filter(_.getName == methodName)(0);
        genExamples(method, null, count)
    }
}

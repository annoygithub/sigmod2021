package scala2c

import scala.meta._
import scala.meta.contrib._
import java.io.PrintWriter
import java.io.File
import scala.collection.mutable.{Map => MMap} 

case class Var(var name: String, var tpe: Type)
case class Klass(tpe: Type, fields: Seq[Var]) {
    val fieldTypes = fields.map(x => x.name -> x.tpe).toMap

    def contains(name: String) = fieldTypes.contains(name)
    def getType(name: String) = fieldTypes(name)
}
case class UDF(var params: Seq[Var],
                var rets: Seq[Var],
                var body: Seq[Stat],
                var klazz: Map[String, Klass] = Map.empty,
                var types: MMap[String, Type] = null,
                var argMap: Seq[String] = null)

case class CUDF(args: Seq[(String, String)],
                rets: Seq[(String, String)],
                body: String, 
                ints: Set[Int],
                doubles: Set[Double],
                strings: Set[String],
                argMap: Seq[String]) {
    def toJson = {
        val jargs = args.map(x => s"""("${x._1}", "${x._2}")""")
        val jrets = rets.map(x => s"""("${x._1}", "${x._2}")""")
        val jretstr = if(jrets.size == 1) jrets(0) else s"[${jrets.mkString(", ")}]"
        var jints = ints.map(x => s"""'"${x}"'""")
        var jintsStr = if (jints.size > 0) s"'ints': [${jints.mkString(", ")}], " else ""
        var jdoubles = doubles.map(x => s"""'"${x}"'""")
        var jdoublesStr  = if (jdoubles.size > 0) s"'doubles': [${jdoubles.mkString(", ")}]," else ""
        var jstrings = strings.map(x => s"""'"${x}"'""")
        var jstringsStr = if (jstrings.size > 0) s"'strings': [${jstrings.mkString(", ")}]," else ""
        var jargMapStr = if (argMap == null) "" else s"'arg_map': [${argMap.map(x=>s""""${x}"""").mkString(", ")}]"
        s"""{
        |   'body': ""${'"'}$body${'"'}"",
        |   'args': [${jargs.mkString(", ")}],
        |   'ret': $jretstr,
        |   $jintsStr
        |   $jdoublesStr
        |   $jstringsStr
        |   $jargMapStr
        |}""".stripMargin.split("\n").filter(_.trim().size > 0).mkString("\n")
    }

    def toPython = {
        s"""
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth(${toJson})
    """
    }
}

object Transpiler {
    def src2UDF(src: String): UDF = {
        val content = scala.io.Source.fromFile(src).mkString
        val oSSA = new SSA()
        val ssa = oSSA.to_ssa(dialects.Sbt1(content).parse[Source].get)
        val regularized = try {
            oSSA.regularize(ssa)
        } catch {
            case e: Throwable =>
                println(s"ssa: $ssa")
                throw e
        }
        val typed = try{
            Typer.infer(regularized)
        } catch {
            case e: Throwable => 
                println(s"regularized: $regularized")
                throw e
        }
        val augmented = try {
            oSSA.augment(typed)
        } catch {
            case e: Throwable =>
                println(s"typed: $typed")
                throw e
        }
        augmented
    }

    def main(args: Array[String]): Unit = {
        if (args.size != 1) {
            println("Usage: scala scala2c.jar <udf.scala>")
            return
        }

        val path = args(0)
        val py = path.split("\\.").reverse.tail.reverse.mkString(".") + ".py"
        val udf = src2UDF(path)
        try {
            new PrintWriter(py){write(ToC.toc(udf).toPython); close}
            println(s"Run `python3 $py comp' to do compositional synthesis")
            println("Please make sure Trinity and CBMC are correctly installed/compiled")
        } catch {
            case e: Throwable =>
                println(s"augmented: $udf")
        }
    }
}

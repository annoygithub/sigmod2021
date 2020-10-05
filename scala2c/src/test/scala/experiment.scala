package scala2c

import scala.meta._
import org.scalatest._
import java.io.PrintWriter
import java.io.File

class ExperimentSpec extends FunSuite {
    val expPath = "/home/gzhang9/code/udf2sql/experiments/udf/"

    def src2UDF(src: String): UDF = {
        val content = scala.io.Source.fromFile(src).mkString
        val oSSA = new SSA()
        val ssa = oSSA.to_ssa(dialects.Sbt1(content).parse[Source].get)
        val regularized = try {
            oSSA.regularize(ssa)
        } catch {
            case e: Throwable =>
                info(s"ssa: $ssa")
                throw e
        }
        val typed = try{
            Typer.infer(regularized)
        } catch {
            case e: Throwable => 
                info(s"regularized: $regularized")
                throw e
        }
        val augmented = try {
            oSSA.augment(typed)
        } catch {
            case e: Throwable =>
                info(s"typed: $typed")
                throw e
        }
        augmented
    }

    val testcases = Seq(
        ("171/udf.scala", (udf: UDF) => None),
        ("173/udf.scala", (udf: UDF) => None),
        ("414/udf.scala", (udf: UDF) => None),
        ("558/udf.scala", (udf: UDF) => None),
        ("928/udf.scala", (udf: UDF) => None),
        ("1024/udf.scala", (udf: UDF) => udf.body match {
            case Seq(
                q"""val $v1 = first + " " """,
                q"""val $v2 = $v3 + second"""
            ) => 
        }),
        ("1072/udf.scala", (udf: UDF) => None),
        ("1483/udf.scala", (udf: UDF) => None),
        ("2636/udf.scala", (udf: UDF) => None),
        ("2792/udf.scala", (udf: UDF) => None),
        ("2793/udf.scala", (udf: UDF) => None),
        ("2826/udf.scala", (udf: UDF) => None),
        ("2940/udf.scala", (udf: UDF) => None),
        ("2977/udf.scala", (udf: UDF) => None),
        ("3052/udf.scala", (udf: UDF) => None),
        ("3197/udf.scala", (udf: UDF) => None),
        ("3338/udf.scala", (udf: UDF) => None),
        ("3515/udf.scala", (udf: UDF) => None),
        ("3531/udf.scala", (udf: UDF) => None),
        ("3558/udf.scala", (udf: UDF) => None),
        ("3563/udf.scala", (udf: UDF) => None),
        ("3828/udf.scala", (udf: UDF) => None),
        ("3837/udf.scala", (udf: UDF) => None),
        ("3885/udf.scala", (udf: UDF) => None),
        ("3954/udf.scala", (udf: UDF) => None),
        ("3976/udf.scala", (udf: UDF) => None),
        ("4048/udf.scala", (udf: UDF) => None),
        ("4371/udf.scala", (udf: UDF) => None),
        ("4668/udf.scala", (udf: UDF) => None),
        ("5155/udf.scala", (udf: UDF) => None),
        ("5174/udf.scala", (udf: UDF) => None),
        ("5233/udf.scala", (udf: UDF) => None),
        ("5367/udf.scala", (udf: UDF) => None),
        ("5599/udf.scala", (udf: UDF) => None),
        ("5615/udf.scala", (udf: UDF) => None),
        ("5640/udf.scala", (udf: UDF) => None),
        ("5765/udf.scala", (udf: UDF) => None),
        ("5961/udf.scala", (udf: UDF) => None),
        ("6019/udf.scala", (udf: UDF) => None),
        ("6063/udf.scala", (udf: UDF) => None),
        ("6076/udf.scala", (udf: UDF) => None),
        ("6082/udf.scala", (udf: UDF) => None),
        ("6808/udf.scala", (udf: UDF) => None),
        ("6832/udf.scala", (udf: UDF) => None),
        ("6997/udf.scala", (udf: UDF) => None),
        ("7260/udf.scala", (udf: UDF) => None),
        ("7296/udf.scala", (udf: UDF) => None),
        ("7477/udf.scala", (udf: UDF) => None),
        ("7694/udf.scala", (udf: UDF) => None),
        ("7698/udf.scala", (udf: UDF) => None),
        ("7703/udf.scala", (udf: UDF) => None),
        ("7704/udf.scala", (udf: UDF) => None),
        ("7783/udf.scala", (udf: UDF) => None),
        ("7788/udf.scala", (udf: UDF) => None),
        ("7941/udf.scala", (udf: UDF) => None),
        ("7956/udf.scala", (udf: UDF) => None),
        ("8284/udf.scala", (udf: UDF) => None),
        ("8298/udf.scala", (udf: UDF) => None),
        ("8346/udf.scala", (udf: UDF) => None),
        ("8354/udf.scala", (udf: UDF) => None),
        ("8720/udf.scala", (udf: UDF) => None),
        ("9141/udf.scala", (udf: UDF) => None),
        ("9272/udf.scala", (udf: UDF) => None),
        ("app_ccyagg/1_2_3.scala", (udf: UDF) => None),
        ("app_ccyagg/4.scala", (udf: UDF) => None),
        ("app_ccyagg/5.scala", (udf: UDF) => None),
        ("app_ccyagg/6.scala", (udf: UDF) => None),
        ("app_ccyagg/7.scala", (udf: UDF) => None),
        ("app_ccyagg/8.scala", (udf: UDF) => None),
        ("app_ccyagg/9.scala", (udf: UDF) => None),
        ("app_wordcount/1.scala", (udf: UDF) => None),
        ("app_wordcount/2.scala", (udf: UDF) => None),
        ("q2/1.scala", (udf: UDF) => None),
        ("q2/2.scala", (udf: UDF) => None),
        ("q8/1.scala", (udf: UDF) => None),
        ("q8/2.scala", (udf: UDF) => None),
        ("q8/3.scala", (udf: UDF) => None),
        ("q8/4.scala", (udf: UDF) => None),
        ("q11/1.scala", (udf: UDF) => None),
        ("q11/2.scala", (udf: UDF) => None),
        ("q11/3.scala", (udf: UDF) => None),
        ("q16/1.scala", (udf: UDF) => None),
        ("q16/2.scala", (udf: UDF) => None),
        ("q17/1.scala", (udf: UDF) => None),
        ("q17/2.scala", (udf: UDF) => None),
        ("q17/3.scala", (udf: UDF) => None),
        ("q19/1.scala", (udf: UDF) => None),
        ("q19/2.scala", (udf: UDF) => None),
        ("q19/3.scala", (udf: UDF) => None),
        ("q19/4.scala", (udf: UDF) => None)
    )

    testcases.foreach(x => 
        test(x._1) {
            val udf = src2UDF(s"$expPath/${x._1}")
            // info(x._1.split("."))
            val py = s"$expPath/${x._1.split("\\.")(0)}.py"
            try{
                x._2(udf)
                new File(py){delete}
                new PrintWriter(py){write(ToC.toc(udf).toPython); close}
            } catch {
                case e: Throwable =>
                    info(s"UDF: $udf")
                    throw e
            }
        }
    )
}

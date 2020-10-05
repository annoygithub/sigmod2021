package scala2c

import scala.meta._
import org.scalatest._

class SSASpec extends FunSuite {
    val ssa = new SSA()
    import ssa._
    test("test") {
        val body="""
            |def udf(first: String, second: String) = {
            |first + ' ' + second
            |}""".stripMargin
    to_ssa(dialects.Sbt1(body).parse[Source].get)
    }
}


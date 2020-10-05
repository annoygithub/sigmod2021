package ast_parser

import java.io.File
import java.io.PrintWriter
import scala.meta._

object Extractor{
    def getTree(p: String) = {
        val path = java.nio.file.Paths.get(p)
        val bytes = java.nio.file.Files.readAllBytes(path)
        val text = new String(bytes, "UTF-8")
        val input = Input.VirtualFile(path.toString, text)
        input.parse[Source].get
    }

    var udf_output_dir = ""
    var unknown_output_dir = ""
    var excluded_output_dir = ""

    val udf_type_r = "(org.apache.spark.sql.Dataset\\[[^\\]]*\\]|org.apache.spark.sql.DataFrame|org.apache.spark.rdd.RDD\\[Row\\]|org.apache.spark.sql.UDFRegistration)".r
    val unknown_type_r = "(error|unknown)".r

    // @param args(0): src
    // @param args(1): type_file
    // @param args(2): udf_ouput_dir
    // @param args(3): unknown_output_dir
    // @param args(4): excluded_output_dir
    def main(args: Array[String]): Unit = {
        val src_tree = getTree(args(0))
        val types = scala.io.Source.fromFile(args(1)).getLines.map(_.split(": ")).map(e => (e(0).trim(), e(1).trim())).toMap
        udf_output_dir = args(2)
        unknown_output_dir = args(3)
        excluded_output_dir = args(4)

        def classify(tpe: String) = {
            tpe match {
                case udf_type_r(_*) => udf_output_dir
                case unknown_type_r(_*) => unknown_output_dir
                case _ => excluded_output_dir
            }
        }

        def short_type(tpe: String) = {
            tpe.split("[\\[\\]]").map(_.split("\\.").last).mkString("-")
        }

        def output(qual: String, call: String, udf: Tree) = {
            val lineno = udf.pos.startLine
            val colno = udf.pos.startColumn
            val tpe = types.getOrElse(qual, "unknown")
            val dir = if (udf.isInstanceOf[Lit.String]) excluded_output_dir else classify(tpe)
            val writer = new PrintWriter(new File(s"$dir/$lineno.$colno.${short_type(tpe)}.$call"))
            
            writer.println(s"Type: $tpe")
            writer.println(s"Call: $call")
            writer.println()
            writer.println(udf)
            writer.close()
        }

        // var i = 0
        def extract(node: Tree) = node match {
            case node @ q"$qual.$func($arg)" => 
                println(s"extracting $node")
                output(qual.toString, func.toString, arg)
            case node @ q"$qual.register($arg1, $arg2)" =>
                println(s"extracting $node")
                output(qual.toString, "register", arg2)
        }

        src_tree traverse {
            case node @ q"$qual.map($arg)" => 
                extract(node)
            case node @ q"$qual.filter($arg)" => 
                extract(node)
            case node @ q"$qual.flatMap($arg)" => 
                extract(node)
            case node @ q"$qual.reduce($arg)" => 
                extract(node)
            case node @ q"$qual.foreach($arg)" => 
                extract(node)
            case node @ q"$qual.foreachPartition($arg)" => 
                extract(node)
            case node @ q"$qual.mapPartitions($arg)" => 
                extract(node)
            case node @ q"$qual.register($arg1,$arg2)" => 
                extract(node)
        }
    }
}

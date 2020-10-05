package ast_parser

import scala.meta._

object Breaker{
    var tid = 0;
    def gettid = {tid += 1; tid}
    def main(args: Array[String]): Unit = {
        val path = java.nio.file.Paths.get(args(0))
        val bytes = java.nio.file.Files.readAllBytes(path)
        val text = new String(bytes, "UTF-8")
        val input = Input.VirtualFile(path.toString, text)
        val exampleTree = input.parse[Source].get

        val transformer = new Transformer {
            def break(node: Tree) = node match {
                case node @ q"$qual.$func($arg)" => 
                    val tname=Term.Name(s"_t_m_p_$gettid")
                    val tqual = this(qual).asInstanceOf[Term]
                    val targ = this(arg).asInstanceOf[Term]
                    val patvar = Pat.Var(tname) :: Nil
                    q"locally{val ..$patvar=$tqual; $tname.$func($targ)}"
                case node @ q"$qual.$func($arg1,$arg2)" => 
                    val tname=Term.Name(s"_t_m_p_$gettid")
                    val tqual = this(qual).asInstanceOf[Term]
                    val targ1 = this(arg1).asInstanceOf[Term]
                    val targ2 = this(arg2).asInstanceOf[Term]
                    val patvar = Pat.Var(tname) :: Nil
                    q"locally{val ..$patvar=$tqual; $tname.$func($targ1, $targ2)}"
            }

            override def apply(tree: Tree): Tree = tree match {
                case node @ q"$qual.map($arg)" => 
                    break(node)
                case node @ q"$qual.filter($arg)" => 
                    break(node)
                case node @ q"$qual.flatMap($arg)" => 
                    break(node)
                case node @ q"$qual.reduce($arg)" => 
                    break(node)
                case node @ q"$qual.foreach($arg)" => 
                    break(node)
                case node @ q"$qual.foreachPartition($arg)" => 
                    break(node)
                case node @ q"$qual.mapPartitions($arg)" => 
                    break(node)
                case node @ q"$qual.register($arg1,$arg2)" => 
                    break(node)
                case node => super.apply(node)
            }
        }

        println(transformer(exampleTree))
    }
}

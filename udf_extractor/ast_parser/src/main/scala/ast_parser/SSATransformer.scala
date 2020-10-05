package ast_parser

import scala.meta._

class SSATransformer extends Transformer {
    override def apply(tree: Tree): Tree = tree match {
        case name @ Term.Name("b") => q"function($name)"
        case node => super.apply(node)
    }
}

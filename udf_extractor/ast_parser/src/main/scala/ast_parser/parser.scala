package ast_parser

import scala.meta._
import scala.collection.mutable

case class TPE(name: String, args: List[TPE] = Nil) 

object TPE{
    def apply(decltpe: Type.Name): TPE = {
        TPE(decltpe.value)
    }

    def apply(decltpe: Type.Apply): TPE = {
        TPE(decltpe.tpe.asInstanceOf[Type.Name].value, decltpe.args.map(TPE(_)))
    }

    def apply(decltpe: Type): TPE = {
        decltpe match {
            case n: Type.Name => apply(n)
            case a: Type.Apply => apply(a)
        }
    }
}

class ExtractorWithTypeInference extends Traverser {
    val scopedVarTypes: mutable.Stack[mutable.Map[String,TPE]] = scala.collection.mutable.Stack[scala.collection.mutable.Map[String, TPE]]()

    var headOfFunc = false

    def enterScope(node: Tree): mutable.Stack[mutable.Map[String,TPE]] = {
        print(f"Entering scope ${node.productPrefix} @ line ${node.pos.startLine}")
        scopedVarTypes.push(scala.collection.mutable.Map[String, TPE]())
    }

    def exitScope(node: Tree): Unit = {
        val types = scopedVarTypes.pop()
        print(f"Exiting scope ${node.productPrefix} @ line ${node.pos.endLine}")
        print(f"-types=$types")
    }

    def addParam(param: Term.Param): Unit = {
        var tpe: TPE = null
        param.decltpe match {
            case None => 
            case t: Some[Type] => tpe = TPE(t.get)
        }
        scopedVarTypes.top(param.name.value) = tpe
        return
    }

    def print(str: String): Unit = {} //println("  " * scopedVarTypes.size + str)

    override def apply(tree: Tree): Unit = tree match {
        case node: Defn.Object =>
            enterScope(node)
            super.apply(node)
            exitScope(node)
        case node:  Defn.Def =>
            enterScope(node)
            headOfFunc = true
            node.paramss.foreach(_.foreach(addParam(_)))
            super.apply(node)
            headOfFunc = false
            exitScope(node)
        case node: Term.Function =>
            enterScope(node)
            headOfFunc = true
            node.params.foreach(addParam(_))
            super.apply(node)
            headOfFunc = false
            exitScope(node)
        case node: Term.Block =>
            if (! headOfFunc) {
                enterScope(node)
                super.apply(node)
                exitScope(node)
            } else {
                headOfFunc = false
            }
        case node @ q"$qual.map($arg)" => 
            println(qual)
            super.apply(node)
        case node @ q"$qual.filter($arg)" => 
            // println(node)
            super.apply(node)
        case node =>
            super.apply(node)
    }
}

object Main{
    val tpeDict: mutable.Stack[scala.collection.Map[String,TPE]] = scala.collection.mutable.Stack[scala.collection.Map[String, TPE]]()
    val extractor = new ExtractorWithTypeInference

    def main(args: Array[String]): Unit = {
        val path = java.nio.file.Paths.get(".", args(0))
        val bytes = java.nio.file.Files.readAllBytes(path)
        val text = new String(bytes, "UTF-8")
        val input = Input.VirtualFile(path.toString, text)
        val exampleTree = input.parse[Source].get

        //extractor(exampleTree)
        if (args(0) == "break") Breaker.main(args)
    }

    def enterScope(): mutable.Stack[scala.collection.Map[String,TPE]] = {
        tpeDict.push(scala.collection.mutable.Map[String, TPE]())
    }

    def exitScope(): scala.collection.Map[String,TPE] = {
        tpeDict.pop()
    }
}

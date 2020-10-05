package scala2c

import scala.meta._
import scala.collection.mutable.{Map => MMap}

object Typer {
    val inferRules = Map(
        ("+", "Double", "Double") -> t"Double",
        ("+", "Int", "Int") -> t"Int",
        ("+", "String", "String") -> t"String",
        ("+", "String", "Char") -> t"String",
        ("+", "String", "Int") -> t"String",
        ("+", "String", "Long") -> t"String",
        ("+", "Unknown", "String") -> t"String",
        ("+", "String", "Unknown") -> t"String",
        ("-", "Double", "Double") -> t"Double",
        ("-", "Int", "Int") -> t"Int",
        ("*", "Double", "Double") -> t"Double",
        ("/", "Double", "Double") -> t"Double",
        ("%", "Long", "Int") -> t"Long",
        ("==", "String", "String") -> t"Boolean",
        ("==", "Double", "Double") -> t"Boolean",
        ("==", "java.lang.Double", "Null") -> t"Boolean",
        ("==", "Int", "Int") -> t"Boolean",
        ("==", "Long", "Int") -> t"Boolean",
        ("!=", "Byte", "Int") -> t"Boolean",
        ("!=", "Null", "String") -> t"Boolean",
        ("!=", "String", "String") -> t"Boolean",
        ("!=", "String", "Null") -> t"Boolean",
        ("!=", "Seq[String]", "Null") -> t"Boolean",
        ("!=", "Long", "Null") -> t"Boolean",
        ("!=", "Long", "Int") -> t"Boolean",
        (">=", "Double", "Double") -> t"Boolean",
        (">=", "Int", "Int") -> t"Boolean",
        (">=", "Long", "Int") -> t"Boolean",
        (">", "Int", "Int") -> t"Boolean",
        (">", "Long", "Int") -> t"Boolean",
        (">", "Double", "Double") -> t"Boolean",
        ("<=", "Double", "Double") -> t"Boolean",
        ("<=", "Long", "Int") -> t"Boolean",
        ("<", "Double", "Double") -> t"Boolean",
        ("&&", "Boolean", "Boolean") -> t"Boolean",
        ("||", "Boolean", "Boolean") -> t"Boolean"
    )

    // def inferCaseType(term: Term, i: Int, klass: Klass): Type = {
    //     term match {
    //         case name: Term.Name => klass.fields(i).tpe
    //         case lit: Lit => inferLitType(lit)
    //     }
    // }

    def inferLitType(lit: Lit): Type = {
        lit match {
            case char: Lit.Char => t"Char"
            case str: Lit.String => t"String"
            case int: Lit.Int => t"Int"
            case d: Lit.Double => t"Double"
            case d: Lit.Boolean => t"Boolean"
            case _: Lit.Null => t"Null"
        }
    }

    def inferType(term: Term, mapFunc: String=>Type): Type = {
        term match {
            case name: Term.Name => mapFunc(name.value)
            case lit: Lit => inferLitType(lit)
        }
    }

    def inferType(term: Term, types: MMap[String, Type]): Type = {
        inferType(term, types.get(_).get)
    }

    def infer(udf: UDF) = {
        val types = MMap[String, Type]()

        def _t(term: Term): Type = {
            inferType(term, types.get(_).get)
        }

        def inferMethod1(obj: Term.Name, method: Term.Name, args: List[Term]):Type = {
            _t(obj) match {
                case t"String" => {
                    method.value match {
                        case "split" => t"Array[String]"
                        case "forall" | "startsWith" | "equals" => t"Boolean"
                        case "replace" | "stripPrefix" | "stripSuffix" | "substring" | "toLowerCase" => t"String"
                        case "indexOf" => t"Int"
                    }
                }
                case t"$t1[$t2]" => {
                    method.value match {
                        case "zip" => t"$t1[($t2, ${_t(args(0)).asInstanceOf[Type.Apply].args(0)})]"
                        case "contains" => t"Boolean"
                        case "intersect" => t"$t1[$t2]"
                        case "toMap" => {
                            val t"($ta1, $ta2)" = t2
                            t"Map[$ta1, $ta2]"
                        }
                        case "map" if t2.toString == "String" && args.size == 1 => {
                            args(0) match {
                                case q"_.trim" => t"$t1[String]"
                            }
                        }
                    }
                }
            }
        }

        def inferMethod(obj: Term.Name, method: Term.Name, args: List[Term]):Type = {
            obj.value match {
                case "math" => {
                    method.value match {
                        case "signum" => t"Int"
                        case "pow" => t"Double"
                    }
                }
                case _ => inferMethod1(obj, method, args)
            }
        }

        def inferFunc(obj: Term.Name, args: List[Term]): Type = {
            obj.value match {
                case "List" => t"List[${_t(args(0))}]"
                case "Seq" => t"Seq[${_t(args(0))}]"
                case "Seq[String]" => t"Seq[String]"
                case _ =>{
                    _t(obj) match {
                        case t"Array[$t]" => t
                    }
                }
            }
        }

        def inferSelect(obj: Term.Name, field: Term.Name): Type = {
            _t(obj) match {
                case t"String" => {
                    field.value match {
                        case "toLong" => t"Long"
                        case "toInt" => t"Int"
                        case "toDouble" | "toFloat" => t"Double"
                        case "trim" | "toLowerCase" => t"String"
                        case "length" => t"Int"
                    }
                }
                case t"Double" => {
                    field.value match {
                        case "toString" => t"String"
                    }
                }
                case t"$t1[$t2]" => {
                    field.value match {
                        case "length" | "size" => t"Int"
                        case "head" => t2
                    }
                }
                case t"($t1, $t2)" => {
                    field.value match {
                        case "swap" => t"($t2, $t1)"
                        case "_1" => t1
                        case "_2" => t2
                    }
                }
                case t"Unknown" => {
                    field.value match {
                        case "toString" => t"String"
                        case "toFloat" => t"Double"
                    }
                }
            }
        }

        udf.params.foreach(p => types(p.name) = p.tpe)
        udf.body.foreach(stat => 
            stat match {
                case q"val ${v: Pat.Var} = $term" => {
                    types(v.name.value) = term match {
                        case q"$lhs $op $rhs" => {
                            val tlhs = _t(lhs).toString
                            val trhs = _t(rhs).toString
                            inferRules((op.value, tlhs, trhs))
                        }
                        case q"${obj:Term.Name}.${method:Term.Name}(..$args)" => inferMethod(obj, method, args)
                        case q"${obj:Term.Name}(..$args)" => inferFunc(obj, args)
                        case q"${t1:Term.Name}[$t2](..$args)" => t"${Type.Name(t1.value)}[$t2]"
                        case q"${obj:Term.Name}.${field:Term.Name}" => inferSelect(obj, field)
                        case q"if($cond) $thenp else $elsep" => if (thenp.toString != "null") _t(thenp) else _t(elsep)
                        case apply: Term.ApplyUnary => {
                            apply.op.value match {
                                case "!" => t"Boolean"
                            }
                        }
                        case q"(..${args:List[Term.Name]})" => t"(..${args.map(a=>_t(a))})"
                        case inter: Term.Interpolate if inter.prefix.value == "s" => t"String"
                        case n: Term.Name => _t(n)
                        case s: Lit.String => t"String"
                        case i: Lit.Int => t"Int"
                        case b: Lit.Boolean => t"Boolean"
                    }
                }
                case _ => 
            }
        )
        udf.types = types
        udf
    }
}

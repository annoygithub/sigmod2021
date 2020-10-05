package scala2c

import scala.meta._

object ToC{
    val typeMap = Map(
        "String" -> "String",
        "Double" -> "double",
        "java.lang.Double" -> "double",
        "Byte" -> "int",
        "Int" -> "int",
        "Long" -> "long",
        "Boolean" -> "_Bool",
        "Any" -> "Any",
        "Array[String]" -> "AString",
        "List[String]" -> "AString",
        "Seq[String]" -> "AString",
        "Set[String]" -> "AString",
        "List[Any]" -> "AAny",
        "Map[String, Any]" -> "MStringAny",
        "List[(String, Any)]" -> "AStringAny",
        "(Long, String)" -> "Tuple",
        "(String, Long)" -> "Tuple"
    )

    def toc(udf: UDF): CUDF = {
        val ints = scala.collection.mutable.Set[Int]()
        val doubles = scala.collection.mutable.Set[Double]()
        val strings = scala.collection.mutable.Set[String]()

        def stat2c(stat: Stat): String = {
            stat match {
                case q"val ${v: Pat.Var} = $term" => {
                    // println(v, term)
                    val scalatv = Typer.inferType(v.name, udf.types)
                    val tv = typeMap(scalatv.toString)
                    term match {
                        case q"$lhs $op $rhs" => applyinfix2c(v, op, lhs, rhs)
                        case apply: Term.ApplyUnary => applyunary2c(v, apply)
                        case q"${func:Term.Name}(..$args)" => func2c(v, func, args)
                        case q"${func:Term.Name}[${t:Type.Name}]()" => 
                            s"$tv ${v.name.value} = A${t.value}0();"
                        case q"${obj:Term.Name}.${method:Term.Name}(..$args)" => method2c(v, obj, method, args)
                        case q"${obj:Term.Name}.${field:Term.Name}" => select2c(v, obj, field)
                        case q"if(${cond}) ${thenp} else ${elsep}" => 
                            s"$tv ${v.name.value} = ${term2c(cond)} ? ${term2c(thenp, tv)} : ${term2c(elsep, tv)};"
                        case q"(${ob1:Term.Name}, ${ob2:Term.Name})" => {
                            val t"($t1, $t2)" = scalatv
                            s"$tv ${v.name.value} = Tuple_construct(${box(ob1.value, t1)}, ${box(ob2.value, t2)});"
                        }
                        case n: Term.Name => s"$tv ${v.name.value} = ${n.value};"
                        case s: Lit.String => s"String ${v.name.value} = ${term2c(s)};"
                        case i: Lit.Int => s"int ${v.name.value} = ${term2c(i)};"
                        case lit: Lit.Boolean => s"_Bool ${v.name.value} = ${term2c(lit)};"
                    }
                }
            }
        }

        def applyunary2c(v: Pat.Var, apply: Term.ApplyUnary) = {
            apply.op.value match {
                case "!" => s"_Bool ${v.name.value} = ! ${term2c(apply.arg)};"
            }
        }

        def select2c(v: Pat.Var, obj: Term.Name, field: Term.Name) = {
            val tpe = Typer.inferType(obj, udf.types)
            val tv = typeMap(Typer.inferType(v.name, udf.types).toString)
            tpe match {
                case t"String" => {
                    field.value match {
                        case "toLong" | "toInt" => s"long ${v.name.value} = String_toint(${obj.value});"
                        case "toDouble" | "toFloat" => s"double ${v.name.value} = String_todouble(${obj.value});"
                        case "toLowerCase" => s"String ${v.name.value} = String_lower(${obj.value});"
                        case _ => s"$tv ${v.name.value} = String_${field.value}(${obj.value});"
                    }
                }
                case t"Double" => {
                    field.value match {
                        case "toString" => s"String ${v.name.value} = String_fromdouble(${obj.value});"
                    }
                }
                case t"Array[String]" => {
                    field.value match {
                        case "length" | "size" => s"int ${v.name.value} = AString_len(${obj.value});"
                        case "head" => s"String ${v.name.value} = AString_get(${obj.value}, 1);"
                    }
                }
                case t"($t1, $t2)" => {
                    field.value match {
                        case "swap" => s"$tv ${v.name.value} = Tuple_swap(${obj.value});"
                        case "_1" => s"$tv ${v.name.value} = ${unbox(s"${obj.value}->_1", t1)};"
                        case "_2" => s"$tv ${v.name.value} = ${unbox(s"${obj.value}->_2", t2)};"
                    }
                }
            }
        }

        def box(term: String, tpe: Type): String = {
            tpe match {
                case t"Long" => s"boxLong($term)"
                case _ => term
            }
        }

        def unbox(term: String, tpe: Type): String = {
            tpe match {
                case t"Long" => s"unboxLong($term)"
                case _ => term
            }
        }

        def func2c(v: Pat.Var, func: Term.Name, args: List[Term]) = {
            val arglist = args.map(term2c(_)).mkString(", ")
            func match {
                case q"List" | q"Seq" => {
                    val tpe = Typer.inferType(args(0), udf.types)
                    args.size match {
                        case 1 => s"A$tpe ${v.name.value} = A${tpe}1($arglist);"
                        case 2 => s"A$tpe ${v.name.value} = A${tpe}2($arglist);"
                        case _ => {
                            val nseg = args.size/2 + args.size%2
                            val parts = (0 until nseg).map(x => {
                                val partargs = args.slice(x*2, x*2+2).map(term2c(_))
                                s"A${tpe} ${v.name.value}_$x = A${tpe}${partargs.size}(${partargs.mkString(", ")});"
                            })
                            val concatvars = (0 until nseg-2).map(x => s"${v.name.value}_c$x") :+ v.name.value
                            var lhsvars = s"${v.name.value}_0" +: concatvars.slice(0, concatvars.size-1)
                            val rhsvars = (0 until nseg-1).map(x => s"${v.name.value}_${x+1}")
                            val concats = concatvars.zip(lhsvars.zip(rhsvars)).map(x => {
                                s"A${tpe} ${x._1} = A${tpe}_concat(${x._2._1}, ${x._2._2});"
                            })
                            (parts ++ concats).mkString("\n")
                        }
                    }
                }
                case _ => {
                    val tpe = Typer.inferType(func, udf.types)
                    tpe match {
                        case t"Array[String]" => s"String ${v.name.value} = AString_get(${func.value}, $arglist);"
                    }
                }
            }
        }

        def method2c1(v: Pat.Var, obj: Term.Name, method: Term.Name, args: List[Term]) = {
            val arglist = (obj +: args).map(term2c(_)).mkString(", ")
            val tobj = Typer.inferType(obj, udf.types)
            val tv = typeMap(Typer.inferType(v.name, udf.types).toString)
            tobj match {
                case t"List[${tobja:Type.Name}]" => {
                    method match {
                        case q"zip" => {
                            val targ = Typer.inferType(args(0), udf.types)
                            targ match {
                                case t"List[${targa:Type.Name}]" => {
                                    val tret = s"A${tobja.value}${targa.value}"
                                    s"$tret ${v.name.value} = ${tret}_zip(${arglist});"
                                }
                            }
                        }
                    }
                }
                case t"List[(${ta1: Type.Name}, ${ta2: Type.Name})]" => {
                    method match {
                        case q"toMap" => {
                            s"M${ta1.value}${ta2.value} ${v.name.value} = A${ta1.value}${ta2.value}_toMap($arglist);"
                        }
                    }
                }
                case t"$t[${t1:Type.Name}]" => {
                    method match {
                        case _ => {
                            s"$tv ${v.name.value} = A${t1.value}_${method.value}($arglist);"
                        }
                    }
                }
                case t"String" => {
                    method match {
                        case q"substring" if args.size == 2 =>
                            s"$tv ${v.name.value} = String_substring2($arglist);"
                        case q"indexOf" if args.size == 2 =>
                            s"$tv ${v.name.value} = String_indexOf2($arglist);"
                        case _ => s"$tv ${v.name.value} = String_${method.value}($arglist);"
                    }
                }
                case t"Int" | t"Long" => {
                    method match {
                        case q"toString" => s"$tv ${v.name.value} = String_fromint($arglist);"
                    }
                }
                case t"Double" => {
                    method match {
                        case q"toString" => s"$tv ${v.name.value} = String_fromdouble($arglist);"
                    }
                }
            }
        }

        def method2c(v: Pat.Var, obj: Term.Name, method: Term.Name, args: List[Term]) = {
            obj.value match {
                case "math" => {
                    method.value match {
                        case "signum" => s"int ${v.name.value} = math_signum(${term2c(args(0))});"
                        case "pow" => s"double ${v.name.value} = math_pow(${term2c(args(0))}, ${term2c(args(1))});"
                    }
                }
                case _ => method2c1(v, obj, method, args)
            }
        }

        def applyinfix2c(v: Pat.Var, op: Term.Name, lhs: Term, rhs: Term): String = {
            val tv = typeMap(Typer.inferType(v.name, udf.types).toString)
            val tlhs = Typer.inferType(lhs, udf.types).toString
            val trhs = Typer.inferType(rhs, udf.types).toString
            op.value match {
                case "+" if tv == "String" => 
                    s"String ${v.name.value} = String_concat(${term2c(lhs)}, ${term2c(rhs)});"
                case "==" if tlhs == "String" && trhs == "String" =>
                    s"_Bool ${v.name.value} = String_equals(${term2c(lhs)}, ${term2c(rhs)});"
                case "!=" if tlhs == "String" && trhs == "String" =>
                    s"_Bool ${v.name.value}_1 = String_equals(${term2c(lhs)}, ${term2c(rhs)});\n" +
                    s"_Bool ${v.name.value} = ! ${v.name.value}_1;"
                case "==" if tlhs == "Null" || trhs == "Null" =>
                    s"_Bool ${v.name.value} = 0;"
                case "!=" if tlhs == "Null" || trhs == "Null" =>
                    s"_Bool ${v.name.value} = 1;"
                case "%" =>
                    s"$tv ${v.name.value} = math_mod(${term2c(lhs)}, ${term2c(rhs)});"
                case _ => s"$tv ${v.name.value} = ${term2c(lhs)} ${op.value} ${term2c(rhs)};"
            }
        }

        def term2c(term: Term, tpe: String = null): String = {
            term match {
                case q"_.isDigit" => "char_isDigit"
                case q"_.trim" => "String_trim"
                case name: Term.Name => name.value
                case str: Lit.String => {
                    val s=str.syntax.slice(1, str.syntax.size-1)
                    strings.add(s)
                    s"""constString("${s.replace("\\", "\\\\")}")"""
                }
                case i: Lit.Int => {
                    ints.add(i.value)
                    i.syntax
                }
                case d: Lit.Double => {
                    doubles.add(d.syntax.toDouble)
                    d.syntax.toDouble.toString
                }
                case b: Lit.Boolean => {
                    if (b.value) "1" else "0"
                }
                case _: Lit.Null => {
                    if (tpe == null)
                        "NULL"
                    else {
                        tpe match {
                            case "int" => "unboxInteger(NULL)"
                            case "long" => "unboxLong(NULL)"
                            case "double" => "unboxDouble(NULL)"
                            case "String" => "constString(NULL)"
                        }
                    }
                }
            }
        }


        CUDF(
            args = udf.params.map(p => (p.name, typeMap(p.tpe.toString))),
            rets = udf.rets.map(p => (p.name, typeMap(udf.types(p.name).toString))),
            body = udf.body.map(stat2c(_)).mkString("\n"),
            ints = ints.toSet,
            doubles = doubles.toSet,
            strings = strings.toSet,
            argMap = udf.argMap
        )
    }
}

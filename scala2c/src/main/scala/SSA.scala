package scala2c

import scala.meta._
import scala.collection.mutable.{Map => MMap, Seq => MSeq}

class SSA {
    val mutables = MMap[String, MSeq[String]]()
    var tid = 0
    def tmpvar = {tid += 1; s"t$tid"}
    def tmppat = Pat.Var(Term.Name(tmpvar))

    def regularize(udf: UDF): UDF = {
        // Get types of columns in Row
        if (udf.params(0).tpe.toString == "Row") {
            val rowterm = Term.Name(udf.params(0).name)
            val (stats, params) = udf.body.map(stat => stat match {
                case q"val ${v:Pat.Var} = $r.getAs[$tpe](${col: Lit.String})" if r.structure == rowterm.structure =>
                    (None, Some((v.name.value, tpe, s"$$${col.value}")))
                case q"val ${v:Pat.Var} = $r.getAs[$tpe](${col: Term.Name})" if r.structure == rowterm.structure =>
                    (None, Some((v.name.value, tpe, s"$${${col.value}}")))
                case q"val ${v:Pat.Var} = $r.getAs(${col: Lit.String}).toString" if r.structure == rowterm.structure =>
                    (None, Some((v.name.value, t"String", s"$$${col.value}")))
                case q"val ${v:Pat.Var} = $r.getLong(${icol:Lit.Int})" if r.structure == rowterm.structure =>
                    (None, Some((v.name.value, t"Long", s"$$_${icol.value+1}")))
                case q"val ${v:Pat.Var} = $r.getString(${icol:Lit.Int})" if r.structure == rowterm.structure =>
                    (None, Some((v.name.value, t"String", s"$$_${icol.value+1}")))
                case q"val ${v:Pat.Var} = $r.getInt(${icol:Lit.Int})" if r.structure == rowterm.structure =>
                    (None, Some((v.name.value, t"Int", s"$$_${icol.value+1}")))
                case q"val ${v:Pat.Var} = $r.getDouble(${icol:Lit.Int})" if r.structure == rowterm.structure =>
                    (None, Some((v.name.value, t"Double", s"$$_${icol.value+1}")))
                case q"val ${v:Pat.Var} = $r(${icol:Lit.Int}).toString" if r.structure == rowterm.structure =>
                    (None, Some((v.name.value, t"String", s"$$_${icol.value+1}")))
                case q"val ${v:Pat.Var} = $r(${icol:Lit.Int})" if r.structure == rowterm.structure =>
                    (None, Some((v.name.value, t"Unknown", s"$$_${icol.value+1}")))
                case q"val ${v:Pat.Var} = $r.isNullAt(${icol:Lit.Int})" if r.structure == rowterm.structure =>
                    (Some(q"val $v = false"), None)
                case _ => (Some(stat), None)
            }).unzip
            udf.body = stats.flatten

            val globalparams = udf.params.slice(1, udf.params.size)
            val fparams = params.flatten
            udf.params = fparams.map(x=>Var(x._1, x._2)) ++ globalparams
            udf.argMap = fparams.map(x=>x._3) ++ globalparams.zipWithIndex.map(x=>s"$$_${x._2 + fparams.size + 1}")
        }

        // Flatten input
        
        def nestedArg = udf.params.filter(x => 
            udf.klazz.contains(x.tpe.toString) ||
            x.tpe.isInstanceOf[Type.Tuple]
        ).map(_.name).toSet
        if (nestedArg.size > 0) {
            assert(udf.argMap == null)
            var argMap = udf.params.zipWithIndex.map(x => 
                x._1.name -> (x._1.tpe, if (udf.params.size > 1) s"_${x._2+1}" else "")
            ).toMap
            while (nestedArg.size > 0) {
                val (stats, params) = udf.body.map(stat => stat match {
                    case q"val ${v:Pat.Var} = ${ob:Term.Name}.${field:Term.Name}" if nestedArg.contains(ob.value) => {
                        val (obtpe, obam) = argMap(ob.value)
                        val fieldtpe = obtpe match {
                            case t: Type.Tuple => t.args(field.value.substring(1).toInt-1)
                            case _ => udf.klazz(obtpe.toString).getType(field.value)
                        }
                        val fieldam = if (obam == "") "$" + field.value else s"$obam.$$${field.value}" 
                        (None, Some((v.name.value, fieldtpe, fieldam)))
                    }
                    case _ => (Some(stat), None)
                }).unzip
                udf.body = stats.flatten
                udf.params = udf.params.filter(x => ! nestedArg.contains(x.name)) ++ 
                    params.flatten.map(x => Var(x._1, x._2))
                argMap = argMap.filter(x => ! nestedArg.contains(x._1)) ++
                    params.flatten.map(x => x._1 -> (x._2, x._3)).toMap
                udf.argMap = udf.params.map(x => argMap(x.name)._2)
            }
        }
        
        def getReturnVar(term: Term, tpe: Type = null) = term match {
            case name: Term.Name => Var(name.value, tpe)
            case lit: Lit => Var(tmpvar, tpe)
        }
        // Flatten output
        val caseVars: Map[String, List[Var]] = udf.body.flatMap(stat => stat match {
            case q"val ${v:Pat.Var} = ${f:Term.Name}(..${args})" if udf.klazz.contains(f.value) => 
                Some(v.name.value -> args.zipWithIndex.map(a => {
                        a._1 match {
                            case q"${name: Term.Name} = $arg" => getReturnVar(arg)
                            case _ => getReturnVar(a._1)
                        }
                    })
                )
            case q"val ${v:Pat.Var} = (..${args})" =>
                Some(v.name.value -> args.zipWithIndex.map(a => getReturnVar(a._1))
                )
            case _ => None
        }).toMap

        var nestedRet = udf.rets.filter(x => caseVars.contains(x.name)).map(_.name).toSet
        while (nestedRet.size > 0) {
            udf.body = udf.body.flatMap(stat => stat match {
                case q"val ${v:Pat.Var} = $f(..$args)" if nestedRet.contains(v.name.value) => {
                    args.zipWithIndex.flatMap(x => x._1 match {
                        case lit: Lit  => Some(q"val ${Pat.Var(Term.Name(caseVars(v.name.value)(x._2).name))} = $lit")
                        case q"$name=${lit:Lit}" => Some(q"val ${Pat.Var(Term.Name(caseVars(v.name.value)(x._2).name))} = $lit")
                        case _ => None
                    })
                }
                case q"val ${v:Pat.Var} = (..${args})" if nestedRet.contains(v.name.value) => {
                    args.zipWithIndex.flatMap(x => x._1 match {
                        case lit: Lit => Some(q"val ${Pat.Var(Term.Name(caseVars(v.name.value)(x._2).name))} = $lit")
                        case _ => None
                    })
                }
                case _ => Seq(stat)
            })
            udf.rets = udf.rets.flatMap(r => 
                if(caseVars.contains(r.name)) 
                    caseVars(r.name)
                else Seq(r)
            )
            nestedRet = udf.rets.filter(x => caseVars.contains(x.name)).map(_.name).toSet
        }

        // Paramatize const values
        // val strings: Map[String, String] = udf.body.flatMap(x => x.collect{
        //         case s: Lit.String => s.value -> s.syntax.substring(1, s.syntax.size-1)
        //     }).toMap
        // if (strings.size == 1 && strings.head._1.size >= 5) {
        //     val argMap = if(udf.argMap == null)
        //         (0 until udf.params.size).map(x => s"$$_${x+1}")
        //     else udf.argMap
        //     udf.argMap = argMap :+ s"'${strings.head._2}'"
        //     val v = tmppat
        //     udf.params = udf.params :+ Var(v.name.value, t"String")
        //     udf.body = udf.body.map(x => x.transform {
        //         case s: Lit.String if s.value == strings.head._1 => v.name
        //     }.asInstanceOf[Stat])
        // }

        udf
    }

    def cast_to_string(term: Term, udf: UDF): Seq[Stat] = {
        val tpe = Typer.inferType(term, udf.types)
        tpe match {
            case t"String" | t"Null" => Seq(term)
            case t"Char" => Seq(Lit.String(term.asInstanceOf[Lit.Char].value.toString))
            case t"Int" | t"Long" | t"Double" => {
                val v = tmppat
                udf.types(v.name.value) = t"String"
                q"val $v = $term.toString()" :: q"${v.name}" :: Nil
            }
            case t"Unknown" if is_param(term, udf) => {
                update_param_type(udf, term.asInstanceOf[Term.Name].value, t"String")
                Seq(term)
            }
        }
    }

    def update_param_type(udf: UDF, name: String, tpe: Type, newname: String = "") = {
        udf.params.foreach(p => 
            if (p.name == name) {
                if (newname != "") p.name = newname
                p.tpe = tpe
            })
        if (udf.types != null) udf.types(name) = tpe
    }

    def is_param(term: Term, udf: UDF): Boolean = {
        if (! term.isInstanceOf[Term.Name]) return false
        for (p <- udf.params) {
            if (p.name == term.asInstanceOf[Term.Name].value) return true
        }
        return false
    }

    def augment(udf: UDF): UDF = {
        assert(udf.types != null)

        udf.body = udf.body.flatMap( stat =>
            stat match {
                case q"val ${v:Pat.Var} = $term" => {
                    term match {
                        case q"$lhs $op $rhs" => {
                            if (op.value == "+" && Typer.inferType(v.name, udf.types).toString == "String") {
                                val (lhsssa, lhsvar) = name_ssa(cast_to_string(lhs, udf))
                                val (rhsssa, rhsvar) = name_ssa(cast_to_string(rhs, udf))
                                (lhsssa ++ rhsssa) :+ q"val $v = $lhsvar $op $rhsvar"
                            } else Seq(stat)
                        }
                        case inter: Term.Interpolate => {
                            inter.prefix.value match {
                                case "s" => {
                                    val (argssas, argvars) = inter.args.map(x => name_ssa(cast_to_string(x, udf))).unzip
                                    val (preparts, lastpart) = inter.parts.splitAt(inter.parts.size-1)
                                    val terms: List[Term] = preparts.zip(argvars).flatMap(x=>
                                        if (x._1.value == "") Seq(x._2) else Seq(x._1, x._2)
                                    ) ++ (if (lastpart(0).value == "") Seq[Term]() else lastpart)
                                    assert(terms.size >= 2)
                                    val resvars: List[Pat.Var] = terms.slice(0, terms.size-2).map(x=>tmppat) :+ v
                                    val lhsvars: List[Term] = terms.head +: resvars.slice(0, resvars.size).map(_.name)
                                    val rhsvars: List[Term] = terms.slice(1, terms.size)
                                    resvars.foreach(x => udf.types(x.name.value) = t"String")

                                    argssas.flatten ++ resvars.zip(lhsvars.zip(rhsvars)).map(x => 
                                         q"val ${x._1} = ${x._2._1} + ${x._2._2}"
                                    )
                                }
                            }
                        }
                        case q"${obj:Term.Name}.toString" if is_param(obj, udf) && 
                            Typer.inferType(obj, udf.types).toString == "Unknown" => {
                            update_param_type(udf, obj.value, t"String", v.name.value)
                            Seq[Stat]()
                        }
                        case q"${obj:Term.Name}.toFloat" if is_param(obj, udf) && 
                            Typer.inferType(obj, udf.types).toString == "Unknown" => {
                            update_param_type(udf, obj.value, t"Double", v.name.value)
                            Seq[Stat]()
                        }
                        case _ => Seq(stat)
                    }
                }
                case q"assert($term)" => Seq[Stat]()
                case _ => Seq(stat)
            }
        )
        udf
    }

    def to_ssa(src: Source): UDF = {
        var udf: UDF = null
        val klazz: MMap[String, Klass] = MMap.empty
        src traverse {
            case q"case class ${name:Type.Name}(..$fields)" => 
                klazz(name.value) = Klass(tpe=name, fields.map(x=> Var(x.name.value, x.decltpe.get)))
            case q"..$mods def ${f:Term.Name}(..$params): $tpeopt = $expr" => udf = to_ssa(params, expr)
            // case q"..$mods def ${f:Term.Name}(..$params) = $expr" => udf = to_ssa(params, expr)
        }
        udf.klazz = klazz.toMap
        udf
    }

    def to_ssa(params: List[Term.Param], expr: Term): UDF = {
        val stats = expr match {
            case block: Term.Block => block_to_ssa(block, endWithVar=true)
        }
        val (body, Seq(ret)) = stats.splitAt(stats.size-1)
        val rets = ret match {
            case name: Term.Name => Seq(Var(name.value, null))
            case tuple: Term.Tuple => tuple.args.map(a => Var(a.asInstanceOf[Term.Name]value, null))
        }
        UDF(
            params.map(
                p => Var(p.name.value, p.decltpe.get)
            ).toSeq,
            rets,
            body
        )
    }

    def block_to_ssa(block: Term.Block, endWithVar: Boolean = false): Seq[Stat] = {
        val stats = block.stats.flatMap(stat_to_ssa(_))
        if (endWithVar) {
            stats.last match {
                case _: Term.Name => stats
                case _: Term.Tuple => stats
                case term: Term => {
                    val (body, Seq(last)) = stats.splitAt(stats.size-1)
                    val tv = Term.Name(tmpvar)
                    body :+ q"val ${Pat.Var(tv)} = ${term}" :+ tv
                }
            }
        } else stats
    }

    def stat_to_ssa(stat: Stat): Seq[Stat] = {
        stat match {
            case q"assert($term)" => Seq[Stat]()
            case q"$a -> $b" => stat_to_ssa(q"($a, $b)")
            case block: Term.Block => block_to_ssa(block)
            case q"val ${v:Pat.Var}: $tpeopt = $rhs" => assign_to_ssa(v, rhs)
            case q"var ${v:Pat.Var}: $tpeopt = $rhs" => {
                mutables(v.name.value) = MSeq(v.name.value)
                assign_to_ssa(v, rhs.get)
            }
            case q"${obj: Term.Name}.getValuesMap[$tpe](List(..${cols: List[Lit.String]}))" => 
                getValuesMap_to_ssa(obj, tpe, cols)
            case q"${row: Term.Name}.getAs(${col: Lit.String}).toString" => Seq(stat)
            case q"${row: Term.Name}.getAs[$tpe]($col)" => Seq(stat)
            case q"${row: Term.Name}.getString[$tpe](${icol: Lit.Int})" => Seq(stat)
            case q"${row: Term.Name}.isNullAt(${icol: Lit.Int})" => Seq(stat)
            case q"${row: Term.Name}(${x:Lit.Int}).toString" => Seq(stat)
            case apply: Term.ApplyUnary => applyunary_to_ssa(apply)
            case apply: Term.ApplyInfix => applyinfix_to_ssa(apply)
            case apply: Term.Apply => apply_to_ssa(apply)
            case select: Term.Select => select_to_ssa(select)
            case m: Term.Match => match_to_ssa(m)
            case inter: Term.Interpolate => interpolate_to_ssa(inter)
            case tuple: Term.Tuple => tuple_to_ssa(tuple)
            case ifterm: Term.If => ifterm_to_ssa(ifterm)
            case term: Term.ApplyType => Seq(term)
            case name: Term.Name => if (mutables.contains(name.value))
                    Seq(Term.Name(mutables(name.value).last)) 
                else Seq(name)
            case str: Lit.String => Seq(str)
            case i: Lit.Int => {
                if (i.value < 10)
                    Seq(i)
                else{
                    val v = tmppat
                    q"val $v = $i" :: v.name :: Nil
                }
            }
            case c: Lit.Char => Seq(Lit.String(c.value.toString))
            case d: Lit.Double => Seq(d)
            case b: Lit.Boolean =>  {
                val v = tmppat
                q"val $v = $b" :: v.name :: Nil
            }
            case n: Lit.Null => Seq(n)
        }
    }

    def match_to_ssa(m: Term.Match): Seq[Stat] = {
        assert(m.cases.forall(x=>x.pat.isInstanceOf[Lit]))
        val (exprssa, exprvar) = name_ssa(stat_to_ssa(m.expr))
        // val (bodyssas, bodyvars) = m.cases.map(c => name_ssa(stat_to_ssa(c.body))).unzip
        val (lbssas, lbvar) = name_ssa(stat_to_ssa(m.cases.last.body))
        val thens = m.cases.slice(0, m.cases.size-1)
        val resvars = m.cases.slice(1, m.cases.size).map(x=>tmppat)
        val elses = resvars.slice(1, resvars.size).map(_.name) :+ lbvar
        (exprssa ++ lbssas ++
        resvars.zip(thens.zip(elses)).reverse.flatMap(x => {
            val (thenssa, thenvar) = name_ssa(stat_to_ssa(x._2._1.body))
            val condvar = tmppat
            thenssa :+
            q"val $condvar = $exprvar == ${x._2._1.pat.asInstanceOf[Lit]}" :+
            q"val ${x._1} = if(${condvar.name}) $thenvar else ${x._2._2}"
        })) :+ resvars(0).name
    }

    def applyunary_to_ssa(apply: Term.ApplyUnary): Seq[Stat] = {
        val (argssa, argvar) = name_ssa(stat_to_ssa(apply.arg))
        argssa :+ Term.ApplyUnary(op=apply.op, arg=argvar)
    }

    def assign_to_ssa(v: Pat.Var, rhs: Term): Seq[Stat] = {
        val rhsssa = stat_to_ssa(rhs)
        val (body, Seq(last: Term)) = rhsssa.splitAt(rhsssa.size-1)
        if (last.isInstanceOf[Term.Name] && body.size > 0) {
            val q"val $x = $term" = body.last
            body.slice(0, body.size-1) :+ q"val $v = $term"
        } else {
            body :+ q"val $v = $last"
        }
    }

    def ifterm_to_ssa(ifterm: Term.If): Seq[Stat] = {
        val (condssa, condvar) = name_ssa(stat_to_ssa(ifterm.cond))

        if (ifterm.thenp.isInstanceOf[Term.Block] &&
            ifterm.thenp.asInstanceOf[Term.Block].stats.size == 1 && 
            ifterm.thenp.asInstanceOf[Term.Block].stats(0).isInstanceOf[Term.Assign] &&
            ifterm.elsep.isInstanceOf[Term.Block] &&
            ifterm.elsep.asInstanceOf[Term.Block].stats.size == 1 && 
            ifterm.elsep.asInstanceOf[Term.Block].stats(0).isInstanceOf[Term.Assign]) {
            val q"{${v1:Term.Name} = $t1}" = ifterm.thenp
            val q"{${v2:Term.Name} = $t2}" = ifterm.elsep
            val tv1 = tmppat
            val tv2 = tmppat
            val thenssa = assign_to_ssa(tv1, t1)
            val elsessa = assign_to_ssa(tv2, t2)
            val tv1a = tmppat
            val tv2a = tmppat
            val m1 = mutables(v1.value)
            val v1ssa = q"val $tv1a = if ($condvar) ${tv1.name} else ${Term.Name(m1.last)}"
            m1(m1.size-1) = tv1a.name.value
            val m2 = mutables(v2.value)
            val v2ssa = q"val $tv2a = if ($condvar) ${Term.Name(m2.last)} else ${tv2.name}"
            m2(m2.size-1) = tv2a.name.value

            (condssa ++ thenssa ++ elsessa) :+ v1ssa :+ v2ssa
        } else {
            val (thenssa, thenvar) = name_ssa(stat_to_ssa(ifterm.thenp))
            val (elsessa, elsevar) = name_ssa(stat_to_ssa(ifterm.elsep))
            condssa ++ thenssa ++ elsessa :+ q"if($condvar) $thenvar else $elsevar"
        }
    }

    def tuple_to_ssa(tuple: Term.Tuple): Seq[Stat] = {
        val (argssas, argvars) = tuple.args.map(x => name_ssa(stat_to_ssa(x))).unzip
        argssas.flatten :+ q"(..$argvars)"
    }

    def interpolate_to_ssa(inter: Term.Interpolate): Seq[Stat] = {
        val (argssas, argvars) = inter.args.map(a => name_ssa(stat_to_ssa(a))).unzip
        argssas.flatten :+ Term.Interpolate(prefix=inter.prefix, parts=inter.parts, args=argvars)
    }

    def getValuesMap_to_ssa(obj: Term.Name, tpe: Type, cols: List[Lit.String]): Seq[Stat] = {
        val keyvar = tmppat
        val colvars = cols.map(x=>tmppat)
        val valuevar = tmppat
        val zipvar = tmppat

        q"val $keyvar = List(..$cols)" +:
        cols.zip(colvars).map{
            case (col, v) => q"val $v = $obj.getAs[$tpe]($col)"
        } :+
        q"val $valuevar = List(..${colvars.map(_.name)})" :+
        q"val $zipvar = ${keyvar.name}.zip(${valuevar.name})" :+
        q"${zipvar.name}.toMap()"
    }

    def applyinfix_to_ssa(apply: Term.ApplyInfix): Seq[Stat] = {
        apply match {
            case q"$lhs $op $rhs" =>{
                val (lhsssa, lhsvar) = name_ssa(stat_to_ssa(lhs))
                val (rhsssa, rhsvar) = name_ssa(stat_to_ssa(rhs))
                (lhsssa ++ rhsssa) :+ q"$lhsvar $op $rhsvar"
            }
            case q"$lhs $op (..$args)" => {
                lhs match {
                    case ltuple: Term.Tuple if ltuple.args.size == args.size && op.value == "==" && args.size > 1 => {
                        val (lhsssas, lhsvars) = ltuple.args.map(x => name_ssa(stat_to_ssa(x))).unzip
                        val (rhsssas, rhsvars) = args.map(x => name_ssa(stat_to_ssa(x))).unzip
                        val cmpvars = ltuple.args.map(x=>tmppat)
                        val cmpstats = cmpvars.zip(lhsvars.zip(rhsvars)).map(x => {
                            q"val ${x._1} = ${x._2._1} == ${x._2._2}"
                        })
                        val aggvars = (1 until cmpvars.size).map(x=>tmppat)
                        val agglhss = cmpvars.head +: aggvars.slice(0, aggvars.size-1)
                        val aggrhss = cmpvars.slice(1, cmpvars.size)
                        val aggstats = aggvars.zip(agglhss.zip(aggrhss)).map(x => {
                            q"val ${x._1} = ${x._2._1.name} && ${x._2._2.name}"
                        })
                        val q"val $lastv = $lastterm" = aggstats.last
                        (lhsssas.flatten ++
                         rhsssas.flatten ++
                         cmpstats ++ 
                         aggstats.slice(0, aggstats.size-1)) :+ q"$lastterm"
                    }
                }
            }
        }
    }

    def name_ssa(stats: Seq[Stat], apply:Boolean = false): (Seq[Stat], Term) = {
        val (head, Seq(last: Term)) = stats.splitAt(stats.size-1)
        last match {
            case name: Term.Name => (head, name)
            case lit: Lit => (head, lit)
            case q"${obj:Term.Name}.${method:Term.Name}" if apply => (head, last)
            case _ => {
                val tv = tmppat
                (head :+ q"val $tv = $last", tv.name)
            }
        }
    }

    def apply_to_ssa(apply: Term.Apply): Seq[Stat] = {
        val q"$func(..$args)" = apply
        val (funcssa, funcvar) = name_ssa(stat_to_ssa(func), apply=true)
        func match {
            case q"$obj.forall" => funcssa :+ q"$funcvar(..$args)"
            case q"$obj.map" => funcssa :+ q"$funcvar(..$args)"
            case q"$obj[$t]" => {
                val (argssas, argvars) = args.map(a => name_ssa(stat_to_ssa(a))).unzip
                argssas.flatten :+ q"$func(..$argvars)"
            }
            case _ => {
                val (argssas, argvars) = args.map(a => a match {
                    case q"$name=$arg" => {
                        val (ssa, v) = name_ssa(stat_to_ssa(arg))
                        (ssa, q"$name=$v")
                    }
                    case _ => name_ssa(stat_to_ssa(a))
                }).unzip
                funcssa ++ argssas.flatten :+ q"$funcvar(..$argvars)"

            }

        }
    }

    def select_to_ssa(select: Term.Select): Seq[Stat] = {
        val q"$obj.$field" = select
        obj match {
            case q"scala" => Seq(q"$field")
            case _ => {
                val (objssa, objvar) = name_ssa(stat_to_ssa(obj))
                objssa :+ q"$objvar.$field"
            }
        }
    }
}

// https://github.com/iodone/rotor/blob/master//engine/src/main/scala/rotor/engine/udf/Functions.scala
def udf(co: String) = {
        val parseMethod = Class.forName("org.ansj.splitWord.analysis.NlpAnalysis").getMethod("parse", classOf[String])
        val tmp = parseMethod.invoke(null, co)
        val terms = tmp.getClass.getMethod("getTerms").invoke(tmp).asInstanceOf[java.util.List[Any]]
        locally {
          val _t_m_p_2 = terms
          _t_m_p_2.map(f => f.asInstanceOf[{ def getName: String }].getName)
        }.toArray
      }

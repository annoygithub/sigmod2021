// https://github.com/XichengDong/sparktraining/blob/master//src/main/scala/org/training/spark/ml/MLUtils.scala
def udf(row: Row) = { 
        val seq = row.toSeq
        val data = locally {
          val _t_m_p_2 = seq.drop(1).dropRight(2)
          _t_m_p_2.map(_.asInstanceOf[String].toDouble)
        }
        (Vectors.dense(data.toArray), seq.last.asInstanceOf[String].toDouble)
      }

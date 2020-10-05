// https://github.com/jeffreyksmithjr/reactive-machine-learning-systems/blob/master//chapter-2/src/main/scala/com/reactivemachinelearning/SparkIntroduction.scala
def udf(line: String) = {
        val parts = line.split(',')
        LabeledPoint(parts(0).toDouble, Vectors.dense(locally {
          val _t_m_p_4 = parts(1).split(' ')
          _t_m_p_4.map(_.toDouble)
        }))
      }

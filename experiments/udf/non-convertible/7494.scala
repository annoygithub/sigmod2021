// https://github.com/Cecca/diversity-maximization/blob/master//experiments/src/main/scala/it/unipd/dei/diversity/matroid/WikiPageLDA.scala
def udf(row: Row) = {
    val vector = locally {
          val _t_m_p_9 = row.getString(row.fieldIndex("vector")).split(" ")
          _t_m_p_9.map(_.toDouble)
        }.toArray
        WikiPageLDA(row.getLong(row.fieldIndex("id")), row.getString(row.fieldIndex("title")), locally {
          val _t_m_p_10 = row.getSeq[Long](row.fieldIndex("topic"))
          _t_m_p_10.map(_.toInt)
        }.toArray, Vectors.dense(vector))
      }

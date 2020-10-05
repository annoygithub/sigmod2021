// https://github.com/uuunic/ProcessVideoInfo/blob/master//src/main/scala/Algorithm/NewProcess.scala
def udf(line: Row) = {
        val vid1 = line.getAs[String](0)
        val sv1 = line.getAs[SV](1)
        val vid_tags = line.getAs[mutable.WrappedArray[String]](2).toArray
        val vid_title = line.getAs[String](3)
        val bsv1 = new SparseVector[Double](sv1.indices, sv1.values, sv1.size)
        val ret = locally {
          val _t_m_p_45 = broadcast_cid_sv.value
          _t_m_p_45.map(line2 => {
            val cid = line2._1
            val sv2 = line2._2
            val cid_tags = line2._3
            val cid_title = line2._4
            val bsv2 = new SparseVector[Double](sv2.indices, sv2.values, sv2.size)
            val cosSim = bsv1.dot(bsv2) / (norm(bsv1) * norm(bsv2))
            (cid, cosSim, cid_tags, sv2, cid_title)
          })
        }.maxBy(_._2)
        cos_result(vid1, ret._1, ret._2, vid_title, ret._5, vid_tags, ret._3, sv1, ret._4)
      }

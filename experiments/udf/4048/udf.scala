// https://github.com/steelxiang/spark-ftp/blob/master//src/main/scala/loaddata/ftp2hdfs_it.scala
case class YHtable(dataSource :Int,
                   URL:String,
                   Id:String,
                   URL_Time:Int,
                   dt        :String)
def udf(t: Row, dataType: Int, filename: String, d: String)  = {
        val line: Array[String] = t.getString(0).split("\t")
        val dataSource: Int = dataType
        var URL: String = line(0)
        var URL_Time: Int = 1
        if (filename.startsWith("lte_cdpi_url") || filename.startsWith("3g_cdpi_url")) {
          URL = line(1)
        } else {
          URL_Time = line(1).toInt
        }
        val Id: String = ""
        val dt: String = d
        YHtable(dataSource, URL, Id, URL_Time, dt)
}

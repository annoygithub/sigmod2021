// https://github.com/Justxiaobu/tbl-bigdata/blob/master//tbl-bigdata-offline/src/main/scala/com/tbl/offline/process/AnalysisLog.scala
def udf(r: Row)  = {
        val pack = s"${r.getString(0)},${r.getString(1)},${r.getString(2)}"
        val command = r.getString(3)
        (pack, command)
}

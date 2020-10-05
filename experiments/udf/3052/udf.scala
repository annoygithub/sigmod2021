// https://github.com/zixuedanxin/bigdata_learn/blob/master//spark-scala-learn/src/main/scala/kafkaDemo/objectProject/dataImportKafkaPerformance.scala
case class eventRow(
                     jioyrq: String,
                     jioysj: String,
                     guiyls: String,
                     cpznxh: String,
                     jiaoym: String,
                     jiedbz: String,
                     jio1je: String,
                     kemucc: String,
                     kehuzh: String,
                     kehhao: String,
                     zhyodm: String,
                     hmjsjc: String,
                     huobdh: String
                   )

def udf(newRow: Row) = {
     eventRow(newRow(0).toString, if (!newRow(1).toString.equals("")) newRow(1).toString else "0", newRow(2).toString, if (!newRow(3).toString.equals("")) newRow(3).toString else "0", newRow(4).toString, newRow(5).toString, if (!newRow(6).toString.equals("")) newRow(6).toString else "0", newRow(7).toString, newRow(8).toString, newRow(9).toString, newRow(10).toString, newRow(11).toString, newRow(12).toString)
}

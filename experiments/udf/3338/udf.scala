// https://github.com/uuunic/ProcessVideoInfo/blob/master//src/main/scala/DataAdapter/UserInterest.scala
def udf(line: Row) = {
          val guid = line.getString(0)
          val first = line.getInt(1)
          val second = line.getInt(2)
          val weight = line.getDouble(3)
          val cat_weight = (first, second, weight)
          (guid, cat_weight)
}

// https://github.com/DITAS-Project/ehealth-sample-spark-vdc/blob/master//app/controllers/EHealthVDCController.scala
  def anyNotNull(row: Row, columnName: String = Constants.SUBJECT_ID_COL_NAME): Boolean = {
    val len = row.length
    var i = 0
    var fieldNames = row.schema.fieldNames
    //print patientId if its the only col
    if (len == 1 && fieldNames(0).equals(columnName))
      return true
    //skip patientId
    for( i <- 0 until len){
      if (!fieldNames(i).equals(columnName) && !row.isNullAt(i)) {
        return true
      }
    }
    false
  }

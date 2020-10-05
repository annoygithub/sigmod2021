// https://github.com/AbsaOSS/enceladus/blob/master//utils/src/main/scala/za/co/absa/enceladus/utils/udf/UDFLibrary.scala
case class Mapping(mappingTableColumn: String, mappedDatasetColumn: String)
case class ErrorMessage(errType: String, errCode: String, errMsg: String, errCol: String, rawValues: Seq[String], mappings: Seq[Mapping] = Seq())

  def confCastErr(errCol: String, rawValue: String, code: String): ErrorMessage = {
    ErrorMessage(
    errType = "confCastError",
    errCode = code,
    errMsg = "Conformance Error - Null returned by casting conformance rule",
    errCol = errCol,
    rawValues = Seq(rawValue))
  }

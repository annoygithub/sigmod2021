// https://github.com/deepsense-ai/seahorse/blob/master//seahorse-workflow-executor/commons/src/main/scala/ai/deepsense/commons/spark/sql/UserDefinedFunctions.scala
def nullSafeSingleParamOp(d: java.lang.Double): java.lang.Double = {
      if (d == null) {
        null
      } else {
        math.signum(d)
      }
  }

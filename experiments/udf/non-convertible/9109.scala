// https://github.com/salesforce/TransmogrifAI/blob/master//features/src/main/scala/com/salesforce/op/stages/base/quaternary/QuaternaryEstimator.scala
def udf(r: Row) = {
    (convertI1.fromSpark(r.get(0)).value, convertI2.fromSpark(r.get(1)).value, convertI3.fromSpark(r.get(2)).value, convertI4.fromSpark(r.get(3)).value)
}

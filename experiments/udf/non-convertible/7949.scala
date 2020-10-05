// https://github.com/JimmyCai/xiaomi-dmc-risk-contest/blob/master//src/main/scala/com/xiaomi/miui/ad/feature_engineering/XGBFeature.scala
def udf(ual: com.xiaomi.miui.ad.others.UALProcessed) = {
    val featureBuilder = new FeatureBuilder
        var startIndex = 1
        startIndex = encodeRateFeatures(featureBuilder, ual, startIndex, queryDetailFieldBroadCast.value, queryDetailRateBroadCast.value, minMaxStatisticsBroadCast.value, 0)(MergedMethod.avg)
        startIndex = encodeRateFeatures(featureBuilder, ual, startIndex, queryStatFieldBroadCast.value, queryStatRateBroadCast.value, minMaxStatisticsBroadCast.value, 0)(MergedMethod.avg)
        startIndex = encodeRateFeatures(featureBuilder, ual, startIndex, appUsageDurationFieldsBroadCast.value, appUsageDurationRateBroadCast.value, minMaxStatisticsBroadCast.value, 0)(MergedMethod.avg)
        startIndex = encodeRateFeatures(featureBuilder, ual, startIndex, appUsageDayFieldsBroadCast.value, appUsageDayRateBroadCast.value, minMaxStatisticsBroadCast.value, 0)(MergedMethod.avg)
        startIndex = encodeRateFeatures(featureBuilder, ual, startIndex, appUsageTimeFieldsBroadCast.value, appUsageTimeRateBroadCast.value, minMaxStatisticsBroadCast.value, 0)(MergedMethod.avg)
        startIndex = encodeRateFeatures(featureBuilder, ual, startIndex, appStatInstallFieldsBroadCast.value, appStatInstallRateBroadCast.value, minMaxStatisticsBroadCast.value, 0)(MergedMethod.avg)
        startIndex = encodeRateFeatures(featureBuilder, ual, startIndex, appStatOpenTimeFieldsBroadCast.value, appStatOpenTimeRateBroadCast.value, minMaxStatisticsBroadCast.value, 0)(MergedMethod.avg)
        startIndex = encodeFeatures(featureBuilder, ual, startIndex, needFieldsBroadCast.value, minMaxStatisticsBroadCast.value, 0)(MergedMethod.avg)
        startIndex = encodeFeatures(featureBuilder, ual, startIndex, needFieldsBroadCast.value, minMaxStatisticsBroadCast.value, 0)(MergedMethod.max)
        startIndex = encodeFeatures(featureBuilder, ual, startIndex, hyAvgFieldsBroadCast.value, minMaxStatisticsBroadCast.value, 6)(MergedMethod.avg)
        startIndex = encodeFeatures(featureBuilder, ual, startIndex, hyMaxFieldsBroadCast.value, minMaxStatisticsBroadCast.value, 6)(MergedMethod.max)
        startIndex = BasicProfile.encode(featureBuilder, ual, startIndex)
        startIndex = MissingValue.encode(featureBuilder, ual, startIndex, 0)
        startIndex = MissingValue.encode(featureBuilder, ual, startIndex, 6)
        FeatureEncoded(ual.user, startIndex - 1, ual.label + featureBuilder.getFeature())
      }
}

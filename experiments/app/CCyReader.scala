// https://github.com/vivekkr/vivekspark/blob/master/src/main/scala/com/spark/ccy/reader/CcyReader.scala
package com.spark.ccy.reader

import org.apache.spark.sql.types._
import org.apache.spark.sql._

/**
  * Created by vivekkr on 02/08/2017.
  */

case class CCYTrade(category: String, customerId: Int, localDate: String, x: String, y: String, z: String, percent: Int)

object CcyReader {

  def main(args: Array[String]) {

    val sparkSession = SparkSession.builder
      .appName("CCY Aggregator")
      .master("local[*]")
      .config("spark.sql.warehouse.dir", "target/ccy-reader")
      .getOrCreate

    import sparkSession.implicits._

    //CNYHKD, 1, 2017-12-09, X, Y, Z,19

    val ccyTradeDS = readDataAndReturnSchema(sparkSession, "src/test/resources/ccy_trade_data.txt")

    val groupByCategory = ccyTradeDS.groupByKey(_.category)
    groupByCategory.keys.show
    val reducedValue: Dataset[(String, Int)] = groupByCategory.mapValues(_.percent).reduceGroups(_ + _)
    reducedValue.foreach(println(_))

    val groupById = ccyTradeDS.groupByKey(_.customerId)
    groupById.keys.show
    val reducedValueById: Dataset[(Int, Int)] = groupById.mapValues(_.percent).reduceGroups(_ + _)
    reducedValueById.foreach(println(_))

    sparkSession.stop()
  }

  def readDataAndReturnSchema(sparkSession: SparkSession, fileLocation: String) = {
    import sparkSession.implicits._

    val row = sparkSession.read.text(fileLocation).as[String]
    // row.collect().foreach(println)

    val ccyTradeDS: Dataset[CCYTrade] = row.map(r => r.split(",").map(_.trim)).map {
      case fields: Array[_] => CCYTrade(fields(0), fields(1).toInt, fields(2), fields(3), fields(4), fields(5), fields(6).toInt)
    }
    ccyTradeDS
  }

}

object U2S {
  val spark = SparkSession.builder
      .appName("CCY Aggregator")
      .master("local[*]")
      // .config("spark.sql.warehouse.dir", "target/ccy-reader")
      .getOrCreate

  case class CCYTrade(category: String, customerId: Int, localDate: String, x: String, y: String, z: String, percent: Int)
  val input = "file:/home/gzhang9/ccy_trade_data.txt"

  def generateInput(n: Long) {
    import org.apache.spark.sql.SaveMode
    spark.range(n).map(i=>s"${i%10000},${i%10000},$i,$i,$i,$i,$i").write.mode(SaveMode.Overwrite).text(input)
  }

  // time used: 19.01s
  def udf() {
    import org.apache.spark.sql.Dataset
    import spark.implicits._
    val row = spark.read.text(input).as[String]
    // row.collect().foreach(println)

    val ccyTradeDS: Dataset[CCYTrade] = row.map(r => r.split(",").map(_.trim)).map {
      case fields: Array[_] => CCYTrade(fields(0), fields(1).toInt, fields(2), fields(3), fields(4), fields(5), fields(6).toInt)
    }
    val groupByCategory = ccyTradeDS.groupByKey(_.category)
    groupByCategory.keys.show
    val reducedValue: Dataset[(String, Int)] = groupByCategory.mapValues(_.percent).reduceGroups(_ + _)
    reducedValue.foreach(println(_))

    val groupById = ccyTradeDS.groupByKey(_.customerId)
    groupById.keys.show
    val reducedValueById: Dataset[(Int, Int)] = groupById.mapValues(_.percent).reduceGroups(_ + _)
    reducedValueById.foreach(println(_))
  }

  // time used: 5.32s
  def sql() {
    import org.apache.spark.sql.Dataset
    import spark.implicits._

    val row = spark.read.text(input).as[String]
    // row.collect().foreach(println)

    val ccyTradeDS: Dataset[CCYTrade] = row.selectExpr(
      "trim(substring_index(value, ',', 1)) as category", 
      "cast(trim(substring_index(substring_index(value, ',', 2), ',', -1)) as int) as customerId",
      "trim(substring_index(substring_index(value, ',', 3), ',', -1)) as localDate",
      "trim(substring_index(substring_index(value, ',', 4), ',', -1)) as x",
      "trim(substring_index(substring_index(value, ',', 5), ',', -1)) as y",
      "trim(substring_index(substring_index(value, ',', 6), ',', -1)) as z",
      "cast(trim(substring_index(substring_index(value, ',', 7), ',', -1)) as int) as percent"
    ).as[CCYTrade]

    ccyTradeDS.groupBy("category").agg(Map[String, String]()).as[String].show

    val reducedValue: Dataset[(String, Int)] = ccyTradeDS.groupBy("category").agg("percent" -> "sum").selectExpr("category", "cast(`sum(percent)` as int)").as[(String, Int)]
    reducedValue.foreach(println(_))

    ccyTradeDS.groupBy("customerId").agg(Map[String, String]()).as[Int].show

    val reducedValueById: Dataset[(Int, Int)] = ccyTradeDS.groupBy("customerId").agg("percent" -> "sum").selectExpr("customerId", "cast(`sum(percent)` as int)").as[(Int, Int)]
    reducedValueById.foreach(println(_))
  }

  def sql1() {
    import org.apache.spark.sql.Dataset
    import spark.implicits._
    val row = spark.read.text(input).as[String]
    // row.collect().foreach(println)

    val ccyTradeDS: Dataset[CCYTrade] = row.selectExpr(
      "trim(substring_index(value, ',', 1)) as category", 
      "cast(trim(substring_index(substring_index(value, ',', 2), ',', -1)) as int) as customerId",
      "trim(substring_index(substring_index(value, ',', 3), ',', -1)) as localDate",
      "trim(substring_index(substring_index(value, ',', 4), ',', -1)) as x",
      "trim(substring_index(substring_index(value, ',', 5), ',', -1)) as y",
      "trim(substring_index(substring_index(value, ',', 6), ',', -1)) as z",
      "cast(trim(substring_index(substring_index(value, ',', 7), ',', -1)) as int) as percent"
    ).as[CCYTrade]
    val groupByCategory = ccyTradeDS.groupByKey(_.category)
    groupByCategory.keys.show
    val reducedValue: Dataset[(String, Int)] = groupByCategory.mapValues(_.percent).reduceGroups(_ + _)
    reducedValue.foreach(println(_))

    val groupById = ccyTradeDS.groupByKey(_.customerId)
    groupById.keys.show
    val reducedValueById: Dataset[(Int, Int)] = groupById.mapValues(_.percent).reduceGroups(_ + _)
    reducedValueById.foreach(println(_))
  }

  def sql2() {
    import org.apache.spark.sql.Dataset
    import spark.implicits._
    val row = spark.read.text(input).as[String]
    // row.collect().foreach(println)

    val ccyTradeDS: Dataset[CCYTrade] = row.map(r => r.split(",").map(_.trim)).map {
      case fields: Array[_] => CCYTrade(fields(0), fields(1).toInt, fields(2), fields(3), fields(4), fields(5), fields(6).toInt)
    }
    ccyTradeDS.groupBy("category").agg(Map[String, String]()).as[String].show

    val reducedValue: Dataset[(String, Int)] = ccyTradeDS.groupBy("category").agg("percent" -> "sum").selectExpr("category", "cast(`sum(percent)` as int)").as[(String, Int)]
    reducedValue.foreach(println(_))

    ccyTradeDS.groupBy("customerId").agg(Map[String, String]()).as[Int].show

    val reducedValueById: Dataset[(Int, Int)] = ccyTradeDS.groupBy("customerId").agg("percent" -> "sum").selectExpr("customerId", "cast(`sum(percent)` as int)").as[(Int, Int)]
    reducedValueById.foreach(println(_))
  }
}

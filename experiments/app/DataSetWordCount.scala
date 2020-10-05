// https://github.com/surendranadhk/surendra_spark_repo/blob/master/SparkProject_V2/src/main/scala/org/spark/training/apiexamples/DataSetWordCount.scala


package org.spark.training.apiexamples

import org.apache.spark.sql.SparkSession

/**
  * Created by hduser on 6/5/16.
  */
object DataSetWordCount {

  def main(args: Array[String]) {

    val sparkSession = SparkSession.builder.
      master("local")
      .appName("example")
      .getOrCreate()

    import sparkSession.implicits._
    val data = sparkSession.read.text("src/main/resources/data.txt").as[String]

    val words = data.flatMap(value => value.split("\\s+"))
   // words.
    //val groupedWords = words.groupByKey(_.toLowerCase)
    val groupedWords = words.groupByKey(_.toLowerCase)

    println(groupedWords.keys)

    val counts = groupedWords.count()

    counts.show()


  }

}

object U2S{
    val spark = SparkSession.builder.
      master("local")
      .appName("example")
      .getOrCreate()

    val input = "file:/home/gzhang9/OnTheOriginOfSpecies.txt.500"

    def generateInput(n: Int) = {
      import org.apache.spark.sql.SaveMode
      spark.read.text(input).as[String].map(value => 
        value.split("\\s+").map(_ + (math.random*n).toInt).mkString(" ")
      ).write.mode(SaveMode.Overwrite).text(s"$input.$n")
    }

    // 2.72s
    def udf() {
        import spark.implicits._
        val data = spark.read.text(input).as[String]
        val words = data.flatMap(value => value.split("\\s+"))
        val groupedWords = words.groupByKey(_.toLowerCase)

        println(groupedWords.keys)

        val counts = groupedWords.count()

        counts.show()
    }

    // 1.99s
    def sql() {
        import spark.implicits._
        val data = spark.read.text(input).as[String]
        val words = data.flatMap(value => value.split("\\s+"))
        val groupedWords = words.selectExpr("value", "lower(value) as key").groupBy("key")

        println(groupedWords.agg(Map[String, String]()).as[String])

        val counts = groupedWords.count()

        counts.show()
    }
}

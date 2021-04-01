package ca.uwaterloo.cs451.a8

import io.bespin.scala.util.Tokenizer

import org.apache.log4j._
import org.apache.hadoop.fs._
import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
import org.rogach.scallop._
import org.apache.spark.Partitioner
import scala.collection.mutable.ListBuffer
import org.apache.spark.HashPartitioner
import scala.collection.mutable._

class TwitterPMIConf(args: Seq[String]) extends ScallopConf(args) {
  mainOptions = Seq(input, output, reducers)
  val input = opt[String](descr = "input path", required = true)
  val output = opt[String](descr = "output path", required = true)
  val reducers = opt[Int](descr = "number of reducers", required = false, default = Some(1))
  // val threshold = opt[Int](descr = "threshold", required = false, default = Some(10))
  verify()
}


object TwitterPMI extends Tokenizer {
  val log = Logger.getLogger(getClass().getName())

  def main(argv: Array[String]) {
    val args = new TwitterPMIConf(argv)

    log.info("Input: " + args.input())
    log.info("Output: " + args.output())
    log.info("Number of reducers: " + args.reducers())

    val conf = new SparkConf().setAppName("TwitterPMI")
    val sc = new SparkContext(conf)
    // val threshold = args.threshold()

    val outputDir = new Path(args.output())
    FileSystem.get(sc.hadoopConfiguration).delete(outputDir, true)

    val inputFile = sc.textFile(args.input(), args.reducers())
    val totalLines = inputFile.count()

    val wordOccur = inputFile
      .flatMap(line => {
        val tokens = tokenize(line)
        if (tokens.length > 0) {
          val wordToSee = 40
          tokens.take(Math.min(tokens.length, wordToSee)).distinct
        }else List()
        })
      .map(word => (word, 1.0f))
      //(x,y) => x + y
      .reduceByKey(_ + _)
      //return the key-value pairs in this RDD to the master as a map
      .collectAsMap()

    val word_count_output = sc.broadcast(wordOccur)

   val pairs = inputFile
      .flatMap(line => {
        val tokens = tokenize(line)
        val wordToSee = 40
        val words = tokens.take(Math.min(tokens.length, wordToSee)).distinct
        if (words.length > 1) {
          //List{(A,B), (A,C), (A,D)...}
          words.flatMap(a => words.map(b => (a, b))).filter(a => a._1 != a._2)
        } else List()
      })
      .map(pair => (pair, 1))
      .reduceByKey(_ + _)
      .sortByKey()
      .filter(p => p._1._1 == "stock" || p._1._2 == "stock")
      val stripes = pairs
        .map(pairs =>(pairs._1._1, pairs._1._2, pairs._2))
        .map(p => {
          var xVal = word_count_output.value(p._1)
          var yVal = word_count_output.value(p._2)
          (p._1, p._2 + "=(" + Math.log10((p._3 * totalLines).toFloat / (xVal * yVal)) + "," + p._3 + ")")
        })
      .groupByKey()
      .map(s => (s._1, s._2.toList.mkString(",")))
      .map(p => "(" + p._1 + "," + " {" + p._2 + "})")
      stripes.saveAsTextFile(args.output())
  }
}

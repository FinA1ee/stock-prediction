# =================================================
# Process stock and tweets data
# =================================================

import pyspark
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, substring,concat
from pyspark.sql.functions import min as sparkMin
import pyspark.sql.functions as F
import pandas as pd
# import datetime, time
from pyspark.sql.window import Window

spark = SparkSession \
    .builder \
    .appName("Stock Price Prediction") \
    .getOrCreate()

# global_setup
# show_description = True
# show_fig = True
# SPLIT_SEED = 12345

# if show_description:
#     print("sparkContext:")
#     print(spark.sparkContext.getConf().getAll())


# =================================================
# 1. Process tweets data
# - created_at column has format: 2021-04-07 17:37:23
# - round it to 2021-04-07 17:37:00 as a join key with stock data
# =================================================

tweets = spark.read.csv("data/tweetParsed/*.csv", header=True) \
    .withColumn("created_at",concat(substring("created_at", 1, 17),lit("00"))) 


# =================================================
# 2. Calculate average stock data
# - combine high, low, open, close price to an average stock price
# - result in a df containing columns ['Datetime','Trend']
# =================================================

window_size = 10

stock = spark.read.csv("data/stock_data_realtime_TSLA.csv", header=True) \
    .withColumn("Average",(col("Open") + col("High") + col("Low") + col("Close")) / lit(4)) \
    .select(col("Datetime"),col("Average")) \
    # .withColumn("Datetime",substring("Datetime", 1, 19))

y_window = Window.partitionBy().orderBy(stock.Datetime)
    # create Post_price column for each Datetime
    # corresponds to creted_at_minute col for tweets data
stock = stock.withColumn("Post_price", F.lead(stock.Average, window_size) \
    .over(y_window))

# calculate the diff, and the trend => 1 for up, 0 for down, 2 for same/null values
stock = stock.withColumn("Trend", \
        F.when(F.isnull(stock.Average - stock.Post_price), 2) \
        # increasing
        .when((stock.Average < stock.Post_price), 1) \
         # decreasing
        .when((stock.Average > stock.Post_price), 0) \
        .otherwise(2)) \
        .select(col("Datetime"),col("Trend"))

# =================================================
# 3. Join stock data with corresponding tweets data
# =================================================

joined_data = tweets.join(stock, tweets.created_at==stock.Datetime) \
    .drop("Datetime") \
    .write.format('csv') \
    .option('header',True) \
    .mode('overwrite') \
    .option('sep',',') \
    .save('data/data_processed')


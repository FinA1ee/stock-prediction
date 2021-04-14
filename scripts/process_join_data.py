# =================================================
# Process stock and tweets data
# =================================================
import sys
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
    
#################  Get commandline args  ################
# target_date = "0409"
target_date = sys.argv[1]
threshold = 1

relative_phrase = ["crypto", "eth", "crypto", "elon", "btc", "musk"]

# =================================================
# 1. Process tweets data
# - created_at column has format: 2021-04-07 17:37:23
# - round it to 2021-04-07 17:37:00 as a join key with stock data
# =================================================

# data by day: 2021-04-07
tweets = spark.read.csv("data/tweet_parsed_"+target_date+"/*.csv", header=True) \
    .withColumn("created_at",substring("created_at", 1, 10))

tweets = tweets.withColumn("hashtags", F.lower("hashtags")) \
    .withColumn("ht_info", lit(""))
    # - clean the hashtag, split it to array of strings
    # - explode to new rows of hashtags
    # - to lower case 
    # - group by hashtag name
    # - filter out ones that occurs more than [threshold] times
# ht = tweets \
#     .withColumn("hashtags", F.regexp_replace("hashtags", "\\[", "")) \
#     .withColumn("hashtags", F.regexp_replace("hashtags", "\\]", "")) \
#     .withColumn("hashtags", F.regexp_replace("hashtags", "\\'", "")) \
#     .withColumn("hashtags", F.split(col("hashtags"), "\\,"))

for word in relative_phrase:
    tweets = tweets.withColumn("ht_info", \
        F.when(tweets.hashtags.contains(lit(word)), concat(tweets.ht_info, lit("1"))) \
        .otherwise(concat(tweets.ht_info, lit("0"))))

########## each row represents a hashtag
# ht_dict =  ht.select(col("hashtags"))
# ht_dict = ht_dict.filter(ht_dict.hashtags!= "[]") \
#     .select("hashtags",F.explode_outer("hashtags")) \
#     .select("col") \
#     .groupBy("col").count() \
#     .select(col("col").alias("hashtag"),col("count").alias("occurance"))
# ht_dict = ht_dict.filter(ht_dict.occurance>=threshold)

# =================================================
# 2. Calculate average stock data
# - combine high, low, open, close price to an average stock price
# - result in a df containing columns ['Datetime','Trend']
# =================================================

# by one day
window_size = 1

stock = spark.read.csv("data/stock_data.csv", header=True) \
    .withColumn("Average",(col("Open") + col("High") + col("Low") + col("Close")) / lit(4)) \
    .select(col("Date"),col("Average"))
    # .withColumn("Datetime",substring("Datetime", 1, 19))

y_window = Window.partitionBy().orderBy(stock.Date)
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
        .select(col("Date"),col("Trend"))

# =================================================
# 3. Join stock data with corresponding tweets data
# =================================================

joined_data = tweets.join(stock, tweets.created_at==stock.Date) \
    .drop("Date") \
    .write.format('csv') \
    .option('header',True) \
    .mode('overwrite') \
    .option('sep',',') \
    .save('data/data_processed')


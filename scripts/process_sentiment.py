# =====================================================
# Assign sentiment score to each tweet by TextBlob
# =====================================================

import pyspark
from textblob import TextBlob
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import col, lit, substring,concat
from pyspark.sql.functions import min as sparkMin
import pyspark.sql.functions as F
import pandas as pd
# import datetime, time
from pyspark.sql.window import Window

if __name__ == "__main__":
    sc = SparkContext(appName="Stock Price Prediction")
    sqlContext = SQLContext(sc)

    schema = StructType([
            StructField("col1", IntegerType(), True),
            StructField("col2", IntegerType(), True),
            StructField("col3", StringType(), True),
            StructField("col4", StringType(), True),
            StructField("col5", StringType(), True),
            StructField("col6", DoubleType(), True)])
    
    rdd = sc.textFile("data/tweetParsed/tweet_data_parsed_2.csv").map(lambda line: line.split(","))
    df = sqlContext.createDataFrame(rdd, schema)
    df.write.parquet('data/tweetParsed/tweet_data_parsed_parquet_2')
    df = sqlCtx.read.load('data/tweetParsed/tweet_data_parsed_parquet_2')
    tweets = df[["id"]]
    tweets.show(3)
# sqlCtx.registerDataFrameAsTable(reviews, "table2")
# reviews1 = sqlCtx.sql("SELECT reviewText, overall from table2")
# #positive->1
# #neutral->0
# #negative->2
# def transform(star):
#         if star >=3.0:
#                 return 1.0
#         elif star == 3.0:
#                 return 0.0
#         else:
#                 return 2.0
# transformer = udf(transform)
# df1 = reviews1.withColumn("label", transformer(reviews['overall']))
# sqlCtx.registerDataFrameAsTable(df1, "table1")
# df2 = sqlCtx.sql("SELECT reviewText, label from table1 WHERE reviewText != ''")
# df2.show()
# def apply_blob(sentence):
#     temp = TextBlob(sentence).sentiment[0]
#     if temp == 0.0:
#         return 0.0
#     elif temp >= 0.0:
#         return 1.0
#     else:
#         return 2.0
# predictions = udf(apply_blob)
# blob_df = df2.withColumn("predicted", predictions(df2['reviewText']))
# blob_df.show()

# true_labels = [i.label for i in blob_df.select("label").collect()]
# predicted_labels = [i.predicted for i in blob_df.select("predicted").collect()]
# correct = 0
# wrong = 0
# for i in range(len(true_labels)):
#         if true_labels[i] == predicted_labels[i]:
#                 correct +=1
#         else:
#                 wrong +=1
# print('Correct predictions: ', correct)
# print('Wrong predictions: ', wrong)
# print('Accuracy: ', correct/(correct+wrong))
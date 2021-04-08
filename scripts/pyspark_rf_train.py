import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession

from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

spark = SparkSession \
    .builder \
    .appName("Stock Price SparkSession") \
    .getOrCreate()

df = spark.read.csv("data/data_processed/*.csv", header=True, inferSchema=True)
df.cache()
df.printSchema()

# sc = SparkContext(appName = "Stock Price SparkContext")
# data = sc.textFile("data/data_processed/*.csv")
# (trainingData, testData) = data.randomSplit([0.7, 0.3])

# model = RandomForest.trainClassifier(trainingData, numClasses=2, categoricalFeaturesInfo={},
#                                      numTrees=3, featureSubsetStrategy="auto",
#                                      impurity='gini', maxDepth=4, maxBins=32)

# data preparation
# categoricalColumns = ['truncated', 'lang']
# stages = []
# for categoricalCol in categoricalColumns:
#     stringIndexer = StringIndexer(inputCol = categoricalCol, outputCol = categoricalCol + 'Index')
#     encoder = OneHotEncoder(inputCols=[stringIndexer.getOutputCol()], outputCols=[categoricalCol + "classVec"])
#     stages += [stringIndexer, encoder]
# label_stringIdx = StringIndexer(inputCol = 'Trend', outputCol = 'label')
# stages += [label_stringIdx]
# numericCols = ['favorite_count', 'retweet_count', 'author_followers_count', 'author_listed_count', \
#     'author_statuses_count', 'author_friends_count', 'author_favourites_count']
# assemblerInputs = [c + "classVec" for c in categoricalColumns] + numericCols
# assembler = VectorAssembler(inputCols=assemblerInputs, outputCol="features")
# stages += [assembler]

# data preparation
train, test = df.randomSplit([0.7, 0.3], seed = 123)
print("Training Dataset Count: " + str(train.count()))
print("Test Dataset Count: " + str(test.count()))

numericCols = ['favorite_count', 'retweet_count', 'author_followers_count', 'author_listed_count', \
    'author_statuses_count', 'author_friends_count', 'author_favourites_count']
assembler = VectorAssembler()\
    .setInputCols(numericCols)\
    .setOutputCol("features")
train_mod01 = assembler.transform(train)

print("first few lines of transformed training data...")
print(train_mod01.limit(5).toPandas())

train_mod02 = train_mod01.select("features","Trend")
all_mod01 = assembler.transform(df)
all_mod02 = all_mod01.select("id","features")
test_mod01 = assembler.transform(test)
test_mod02 = test_mod01.select("id","features")

# train
rfClassifer = RandomForestClassifier(labelCol = "Trend", numTrees = 3)
pipeline = Pipeline(stages = [rfClassifer])
paramGrid = ParamGridBuilder()\
   .addGrid(rfClassifer.maxDepth, [1, 2, 4])\
   .addGrid(rfClassifer.minInstancesPerNode, [1, 2, 4])\
   .build()
evaluator = MulticlassClassificationEvaluator(labelCol = "Trend", predictionCol = "prediction", metricName = "accuracy")
# 10 folds cv
crossval = CrossValidator(estimator = pipeline,
                          estimatorParamMaps = paramGrid,
                          evaluator = evaluator,
                          numFolds = 5)
# final model
cvModel = crossval.fit(train_mod02)
print("best cv prediction accuracy by all 'paramGrid' metrics")
print(cvModel.avgMetrics)

# predict (this part should be prediction on the "actual" test data, instead of all data for now (since we do not have test data yet))
prediction = cvModel.transform(all_mod02)
print("first few lines of prediction...")
print(prediction.limit(5).toPandas())
final_pred = prediction.select("id","prediction")
final_pred.toPandas().to_csv('data/data_prediction/predict_rf.csv',index=False)
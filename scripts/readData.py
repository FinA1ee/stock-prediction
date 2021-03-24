# How to run: python readData.py

import json
import sys
import pandas as pd
  

pd.set_option('max_colwidth',1000)
# pd.set_option('max_rowwidth',1000)

tweets_data_path = '../data/tweetRaw'

tweets_data = []
try:
    tweets_file = open(tweets_data_path, "r")
except IOError:
    print "Error: can't open file"

for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

tweets = pd.DataFrame()
tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
print(tweets['text'].values[0].encode('utf-8'))
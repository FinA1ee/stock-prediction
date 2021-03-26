import json
import sys
import pandas as pd

pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_row', 1000)

# set output path
output_path = '../data/tweetParsed.csv'
sys.stdout = open(output_path, 'w')

# set input path
input_path = '../data/tweetRaw'

# open file
tweets_data = []
try:
    tweets_file = open(input_path, "r")
except IOError:
    print "Error: can't open file"

# read into json format
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

# use pandas to format data
tweets = pd.DataFrame()
# outtweets = [[tweet['created_at'], 
#               tweet['extended_tweet']['full_text'].encode('utf-8') if tweet['truncated'] else tweet['text'].encode('utf-8')]
#              for tweet in tweets_data]

tweets['id'] = map(lambda tweet: tweet['id'], tweets_data)
tweets['created_at'] = map(lambda tweet: tweet['created_at'], tweets_data)
tweets['favorite_count'] = map(lambda tweet: tweet['favorite_count'], tweets_data)
tweets['retweet_count'] = map(lambda tweet: tweet['retweet_count'], tweets_data)
tweets['text'] = map(lambda tweet: tweet['extended_tweet']['full_text'].encode('utf-8') if tweet['truncated'] else tweet['text'].encode('utf-8'), tweets_data)

df = pd.DataFrame(tweets,columns=["id", "created_at", "favorite_count", "retweet_count", "text"])
df.to_csv('tweetsParsed.csv',index=False)

# extract all text
# i = 0
# while i < len(tweets_data):
#     text = tweets['text'].values[i].encode('utf-8').replace("\n", ". ") # remove line breakers
#     if text[0:2] != 'RT':
#         print(text + '\n')
#     i += 1
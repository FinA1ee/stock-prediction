import json
import sys
import tweepy
import pandas as pd

#Variables that contains the user credentials to access Twitter API 
access_token = "950545014542741504-uToPAGQNxW5GWYcEhVmSl1HZiRYbKVM"
access_token_secret = "Eg6CJE9nkTPIHGTa0m1WBGUhd7GqZjMyTUkVsBnql5NxZ"
consumer_key = "w01zE83UD0sGGWukEgpUitoep"
consumer_secret = "tARyuJvmBIZlCrgygzfgY1SmzpymLYMJcZL5o4eQ7JVf72U403"

pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_row', 1000)

# set input path
input_path = 'data/tweet_data_raw'

# set output oath
output_path = 'data/tweet_data_content'
sys.stdout = open(output_path, 'w')

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# open file
tweet_ids = []
try:
    tweets_file = open(input_path, "r")
except IOError:
    print "Error: can't open file"

# read into json format
for line in tweets_file:
    try:
        id = json.loads(line)['id']
        tweet_ids.append(id)
    except:
        continue

tweet_dict = {}
tweet_dict['text'] = []
tweet_dict['retweet_count'] = []
tweet_dict['favorite_count'] = []

# extract info from raw data 
for id in tweet_ids:
    try:
        status = api.get_status(id)
        tweet_dict['text'].append(status.text)
        tweet_dict['retweet_count'].append(status.retweet_count)
        tweet_dict['favorite_count'].append(status.favorite_count)
    except:
        continue

# print info
i = 0
while i < len(tweet_ids):
    likes = tweet_dict['favorite_count'][i]
    retweets = tweet_dict['retweet_count'][i]
    text = tweet_dict['text'][i].encode('utf-8').replace("\n", ". ") # remove line breakers
    print(likes, retweets, text)
    i += 1

# # use pandas to format data
# tweets = pd.DataFrame()
# # outtweets = [[tweet['created_at'], 
# #               tweet['extended_tweet']['full_text'].encode('utf-8') if tweet['truncated'] else tweet['text'].encode('utf-8')]
# #              for tweet in tweets_data]

# tweets['id'] = map(lambda tweet: tweet['id'], tweets_data)
# tweets['created_at'] = map(lambda tweet: tweet['created_at'], tweets_data)
# tweets['favorite_count'] = map(lambda tweet: tweet['favorite_count'], tweets_data)
# tweets['retweet_count'] = map(lambda tweet: tweet['retweet_count'], tweets_data)
# tweets['text'] = map(lambda tweet: tweet['extended_tweet']['full_text'].encode('utf-8') if tweet['truncated'] else tweet['text'].encode('utf-8'), tweets_data)

# df = pd.DataFrame(tweets,columns=["id", "created_at", "favorite_count", "retweet_count", "text"])
# df.to_csv("data/tweet_data_parsed.csv",index=False)

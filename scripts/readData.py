import json
import sys
import pandas as pd

pd.set_option('max_colwidth',1000)

# set output path
output_path = '../data/tweetParsed'
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
tweets['text'] = map(lambda tweet: tweet['extended_tweet']['full_text'] if tweet['truncated'] else tweet['text'], tweets_data)

# extract all text
i = 0
while i < len(tweets_data):
    text = tweets['text'].values[i].encode('utf-8').replace("\n", ". ") # remove line breakers
    if text[0:2] != 'RT':
        print(text + '\n')
    i += 1
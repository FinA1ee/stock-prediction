import logging
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


if __name__ == '__main__':

    logger = logging.getLogger("Read Script")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # parse arguments
    if len(sys.argv) != 3:
        print("Wrong Number of Arguments")
        sys.exit(1)

    # set input path
    input_path = str(sys.argv[1])
    output_path = str(sys.argv[2])
    sys.stdout = open(output_path, 'w')

    logger.info("Handing File: " + input_path)
    logger.info("Output to: " + output_path)

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
    tweet_dict['author_followers_count'] = []
    tweet_dict['author_friends_count'] = []
    tweet_dict['hashtag_indices'] = []

    # extract info from raw data
    size = 0
    for id in tweet_ids:
        try:
            status = api.get_status(id)
            tweet_dict['text'].append(status.text)
            tweet_dict['retweet_count'].append(status.retweet_count)
            tweet_dict['favorite_count'].append(status.favorite_count)
            tweet_dict['author_followers_count'].append(status.author.followers_count)
            tweet_dict['author_friends_count'].append(status.author.friends_count)
            tweet_hashtags = []
            for hashtag in status.entities['hashtags']:
                tweet_hashtags.append(hashtag['indices'])
            tweet_dict['hashtag_indices'].append(tweet_hashtags)
            size += 1
        except:
            continue

    # print info
    i = 0
    while i < size:
        likes = tweet_dict['favorite_count'][i]
        retweets = tweet_dict['retweet_count'][i]
        text = tweet_dict['text'][i].encode('utf-8').replace("\n", ". ") # remove line breakers
        followers = tweet_dict['author_followers_count'][i]
        friends = tweet_dict['author_friends_count'][i]
        hashtags = tweet_dict['hashtag_indices'][i]
        print(likes, retweets, text, followers, friends, hashtags)
        i += 1
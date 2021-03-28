# ensure that you already installed yfinance library
# pip install tweepy

import json
import tweepy
import time
import sys

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "950545014542741504-uToPAGQNxW5GWYcEhVmSl1HZiRYbKVM"
access_token_secret = "Eg6CJE9nkTPIHGTa0m1WBGUhd7GqZjMyTUkVsBnql5NxZ"
consumer_key = "w01zE83UD0sGGWukEgpUitoep"
consumer_secret = "tARyuJvmBIZlCrgygzfgY1SmzpymLYMJcZL5o4eQ7JVf72U403"

class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    # set runtime
    runtime = 30
    if len(sys.argv) == 2:
        runtime = int(sys.argv[1])
        if runtime < 1 or runtime > 1000:
            print("Bad Running time")
            sys.exit(1)
    elif len(sys.argv) > 2:
        print("Wrong Number of Arguments")
        sys.exit(1)

    # set output path
    output_path = 'data/tweet_data_raw'
    sys.stdout = open(output_path, 'w')

    # add listener
    l = StdOutListener()

    # create stream
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, tweet_mode='extended')

    # filter on key words
    stream.filter(track=['tesla', 'elonmusk', 'spacex', 'elon', 'musk'], is_async=True)
    time.sleep(runtime)
    stream.disconnect()

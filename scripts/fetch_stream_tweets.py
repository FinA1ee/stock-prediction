# ensure that you already installed yfinance library
# pip install tweepy
import logging
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

# keywords = ['#tesla', '#spacex', '#elon', '#elonmusk', '#autopilot', 'tesla', 'elon', 'spacex, autopilot']
keywords = ['#teala', 'tesla']
output_path = 'data/tweet_data_raw'

class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    logging.info("Script Running...")

    # set runtime
    runtime = 10
    output_path = 'data/tweet_data_raw'

    if len(sys.argv) > 3:
        print("Wrong Number of Arguments")
        sys.exit(1)
    
    if len(sys.argv) == 3:
        runtime = int(sys.argv[1])
        output_path = str(sys.argv[2])
    elif len(sys.argv) == 2:
        runtime = int(sys.argv[1])


    logging.info("Runtime: " + str(runtime))
    logging.info("Output: " + output_path)

    # set output path
    sys.stdout = open(output_path, 'w')

    # add listener
    l = StdOutListener()

    # create stream
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, tweet_mode='extended')

    # filter on key words
    try:
        stream.filter(track=keywords, is_async=True)
    except:
        sys.exit()
    
    for i in range(runtime):
        logging.info("Fetching..." + str(i))
        time.sleep(1)
    stream.disconnect()

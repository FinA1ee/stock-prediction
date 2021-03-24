import json
import tweepy
import time

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
        print status

if __name__ == '__main__':

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['tesla', 'elonmusk'])

    # # calling the api
    # api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # # the screen_name of the targeted user 
    # screen_name = "elonmusk"

    # # fetching the user 
    # user = api.get_user(screen_name) 

    # # fetch the user id
    # user_id = user.id_str

    # # extract last 3 tweets
    # tweets = api.user_timeline(
    #     # user_id=user_id,
    #     # screen_name=screen_name,
    #     count=200,
    #     include_rts=False,
    #     exclude_replies=True,
    #     tweet_mode='extended'
    # )

    # # extract the latest 600 tweets from elon
    # all_tweets = []
    # all_tweets.extend(tweets)
    # oldest_id = tweets[-1].id

    # n = 0
    # while n < 10:
    #     tweets = api.user_timeline(
    #         # user_id=user_id,
    #         # screen_name=screen_name,
    #         count=200,
    #         include_rts=False,
    #         max_id=oldest_id - 1, 
    #         exclude_replies=True,
    #         tweet_mode='extended'
    #     )
        
    #     if len(tweets) == 0:
    #         n += 1
    #         continue

    #     oldest_id = tweets[-1].id
    #     all_tweets.extend(tweets)
    #     n += 1

    # for info in all_tweets:
    #     year = info.created_at.date().year
    #     month = info.created_at.date().month
    #     if info.favorite_count > 10000 and year == 2020:
    #         # print("ID: {}".format(info.id))
    #         print(info.created_at.date())
    #         # print(info.full_text.encode('utf-8'))
    #         print("Favourite: ", info.favorite_count)
    #         # print("Retweet: ", info.retweet_count)
    #         print("\n")

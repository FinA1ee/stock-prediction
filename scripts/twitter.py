import json
import tweepy

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "950545014542741504-uToPAGQNxW5GWYcEhVmSl1HZiRYbKVM"
access_token_secret = "Eg6CJE9nkTPIHGTa0m1WBGUhd7GqZjMyTUkVsBnql5NxZ"
consumer_key = "w01zE83UD0sGGWukEgpUitoep"
consumer_secret = "tARyuJvmBIZlCrgygzfgY1SmzpymLYMJcZL5o4eQ7JVf72U403"

if __name__ == '__main__':

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # calling the api
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # the screen_name of the targeted user 
    screen_name = "elonmusk"

    # fetching the user 
    user = api.get_user(screen_name) 

    # fetch the user id
    user_id = user.id_str

    # extract the latest 600 tweets from elon
    n = 0
    while n < 3:
        tweets = api.user_timeline(
            user_id=user_id,
            screen_name=screen_name,
            count=200,
            include_rts=False,
            exclude_replies=True,
            tweet_mode='extended'
        )
        
        for info in tweets:
            print("ID: {}".format(info.id))
            print(info.created_at)
            print(info.full_text.encode('utf-8'))
            print("\n")

        n += 1

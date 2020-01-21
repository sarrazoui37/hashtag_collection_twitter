import pprint
import tweepy
from tweepy import OAuthHandler, StreamListener
import csv

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""


class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    
    hashtags_dict = {}
    screen_name=str(input())
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

# indicates the twitter use you would like to gather info from
# the pinned tweet counts as a tweet
    tweets = api.user_timeline(screen_name, count=1500, exclude_replies=True, tweet_mode="extended")


# loops through each hashtag collected from tweets and adds them as a key into the
# hashtags_dict dictionary and adds 1 to the value each time that hashtag is found
# this will not include retweeted hashtags. Only actual tweets for the user.
    for tweet in tweets:
        hashtags = tweet.entities.get('hashtags')
        for hashtag in hashtags:
            upperhashtag=hashtag['text'].upper()
            if upperhashtag in hashtags_dict.keys():
                hashtags_dict[upperhashtag] += 1
            else:
                hashtags_dict[upperhashtag] = 1


    better_hashtag_dict = [{"hashtag":keys,"count":values} for keys,values in zip(hashtags_dict.keys(),hashtags_dict.values())]

    with open("tweet_hashtags.csv", "w", newline='') as tweet_hashtags:
        write=csv.DictWriter(tweet_hashtags,fieldnames=better_hashtag_dict[0].keys())
        write.writeheader()
        write.writerows(better_hashtag_dict)    
    
    pprint.pprint(hashtags_dict)
    print(better_hashtag_dict)
    

from tweepy import Stream
import logging
import time
import tweepy
import os
from dotenv import load_dotenv

# load our .env file to make use of the environment variables
load_dotenv()

# import and assign our environment variables
API_KEY = os.getenv('twitter_api_key')
API_SECRET = os.getenv('twitter_api_secret')
ACCESS_TOKEN = os.getenv('twitter_access_token')
TOKEN_SECRET = os.getenv('twitter_access_token_secret')

# print(API_SECRET, API_KEY, ACCESS_TOKEN, TOKEN_SECRET)

# instantiate oauth handler and set access token
twitter_oauth = tweepy.OAuthHandler(API_KEY, API_SECRET)
twitter_oauth.set_access_token(ACCESS_TOKEN, TOKEN_SECRET)

# instantiate tweepy api object using the authentication handler object
api = tweepy.API(twitter_oauth, wait_on_rate_limit=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# blocked_people = [] 
blocked_words = ["sex", "fuck"]

# attempt credential verification. prints exception if something is wrong
try:
    # print(twitter_api.verify_credentials())
    print("Successfully logged in as", logger)
except tweepy.TweepError as e:
    print(e)
except Exception as e:
    print(e)


class FavRetweetListener(Stream):
    def on_status(self, status):
        print(status.id)

    def contains_hate_words(self, tweet):
        for word in blocked_words:
            if word in tweet:
                return True
            else:
                return False

    def is_reply(self, tweet):
        if tweet.in_reply_to_status_id is not None:
            return True
        else:
            return False

    # this method handles all the tweeting
    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        # print("Yay", tweet)
        file = "log.txt"

        with open(file, "a+", encoding='utf-8') as f:
            if tweet.id not in f:
                f.write(str(f"{tweet.id}\n"))

        if self.contains_hate_words(tweet.text) or self.is_reply(tweet):
            return
        else:
            try:
                api.retweet(tweet.id)
                api.create_favorite(tweet.id)
                time.sleep(60)
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)

    def on_limit(self, status):
        print("Rate Limit Exceeded, Sleep for 15 Mins")
        time.sleep(15 * 60)
        return True

    # Avoid Repeated Tweets
    # FILE_NAME = 'last_seen.txt'
    #
    # def read_last_seen(self, FILE_NAME):
    #     file_read = open(FILE_NAME, 'r')
    #     last_seen_id = int(file_read.read().strip())
    #     file_read.close()
    #     return last_seen_id
    #
    # def store_last_seen(self, FILE_NAME, last_seen_id):
    #     file_write = open(FILE_NAME, 'w')
    #     file_write.write(str(last_seen_id))
    #     file_write.close()
    #     return


# our main function
def main(keywords):
    # api = create_api()
    tweets_listener = FavRetweetListener(API_KEY, API_SECRET, ACCESS_TOKEN, TOKEN_SECRET)
    tweets_listener.filter(track=keywords, languages=["en"])
    return tweets_listener


if __name__ == "__main__":
    main(["Tech", "Coding", "Python", "Uganda Tech", "AfroBoyUg",
          "Fintechs", "Cyber Security", "Hacking", "NFTs", "Blockchain",
          "#100DaysOfCode", "#CodeNewBie", "Google", "Programmer", "computers",
          "Amazon", "AWS", "Cloud Computing", "Cyber", "Metaverse", "DeFi",
          "Crypto", "Bitcoin", "AR", "VR", "Robots", "iot", "Twitter Bots"])

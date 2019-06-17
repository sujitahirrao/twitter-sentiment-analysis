import re
import sys
import datetime as dt
from textblob import TextBlob

from config import Config
from ts_logger import logger
from query import query_tweets


class Tweeter:

    def __init__(self):
        pass

    @staticmethod
    def clean_tweet(tweet_text):
        """
        remove links, special characters using simple regex statements.
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])"
                               "|(\w+:\/\/\S+)", " ", tweet_text).split())

    def get_tweet_sentiment(self, tweet):
        """
        classify sentiment of passed tweet using textblob's sentiment method
        """
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, handle, count):
        """
        fetch tweets and parse them.
        """
        # empty list to store parsed tweets
        tweets = []

        try:
            # print("Number of days:\t", (END_DATE - BEGIN_DATE).days)
            start_time = dt.datetime.now()
            # call twitter api to fetch tweets
            for tweet in query_tweets("to:%s" % handle, count, begindate=Config.BEGIN_DATE,
                                      enddate=Config.END_DATE)[:count]:
                if len(tweet.text) < 5:
                    continue

                # for tweet in query_tweets("to:%s" % handle, begindate=BEGIN_DATE, enddate=END_DATE):
                # print("\n")
                # print("***", tweet.user, "-->", tweet.timestamp, "***")
                # print(tweet.text)
                # print("-->", tweet.replies)

                # empty dictionary to store required params of a tweet
                parsed_tweet = dict()

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                parsed_tweet['timestamp'] = tweet.timestamp
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                tweets.append(parsed_tweet)
            end_time = dt.datetime.now()
            print("\n\nTime Taken to scrape %s tweets:" % len(tweets), end_time - start_time)
            return tweets
        except Exception as e:
            print("Exception : " + str(e))
            logger.error(str(e))


def main(handle):
    # creating object of TwitterClient Class
    tweeter = Tweeter()

    # calling function to get tweets
    tweets = tweeter.get_tweets(handle=handle, count=Config.COUNT)

    if len(tweets) == 0:
        print("No tweets found for this account with current settings.")
        return

    # picking positive tweets from tweets
    pos_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

    # picking negative tweets from tweets
    neg_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    # # printing first 5 positive tweets
    # print("\n\nPositive tweets:")
    # for i, tweet in enumerate(pos_tweets):
    #     print(i, '.\t', tweet['text'])

    # # printing first 5 negative tweets
    # print("\n\nNegative tweets:")
    # for i, tweet in enumerate(neg_tweets):
    #     print(i, '.\t', tweet['text'])

    # percentage of positive tweets
    print("\n\nPositive tweets percentage: {} %".format(100 * len(pos_tweets) / len(tweets)))

    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(neg_tweets) / len(tweets)))

    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % ".format(
        100 * (len(tweets) - len(neg_tweets) - len(pos_tweets)) / len(tweets)))

    print("\n\n")
    print("Total number of tweets: ", len(tweets))
    print("Number of positive tweets: ", len(pos_tweets))
    print("Number of negative tweets: ", len(neg_tweets))
    print("Number of Neutral tweets: ", len(tweets) - len(neg_tweets) - len(pos_tweets))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        tw_handle = str(sys.argv[1])
        # calling main function
        main(tw_handle)
    else:
        print("Please provide the Twitter handle.")

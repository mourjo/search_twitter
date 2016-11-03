#! /usr/bin/env python
import twitter
from util import is_retweet_with_hashtag
from functools import partial


class TwitterClient:
    def __init__(self,
                 consumer_key=None,
                 consumer_secret=None,
                 token=None,
                 token_secret=None):
        "Instantiate the client with the access keys."
        auth = twitter.OAuth(consumer_key=consumer_key,
                             consumer_secret=consumer_secret,
                             token=token,
                             token_secret=token_secret)
        self.conn = twitter.Twitter(auth=auth)

    def __remove_bad_tweets(self, tweets, hashtag):
        "Remove unretweeted tweets and tweets not containing the hashtag.\
        (For some reason the search API does not always return\
        correct results.)"
        return filter(partial(is_retweet_with_hashtag, hashtag),
                      tweets["statuses"])

    def fetch_retweets_with_hashtag(self, hashtag, n=100):
        "Search retweets from using the Twitter REST API which have a hashtag."
        hashtag = hashtag if hashtag.startswith("#") else "#" + hashtag
        search_query = hashtag.lower() + " min_retweets:1"
        tweets = self.conn.search.tweets(q=search_query,
                                         include_entities=True,
                                         count=n,
                                         result_type="mixed")
        tweets_with_hashtags = self.__remove_bad_tweets(tweets,
                                                        hashtag[1:])
        return tweets_with_hashtags

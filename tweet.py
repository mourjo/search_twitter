#! /usr/bin/env python
import twitter


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
        filter_fn = (lambda tweet:
                     (any(htag["text"].lower() == hashtag
                          for htag in tweet["entities"]["hashtags"])
                      and tweet["retweet_count"] > 0))

        return filter(filter_fn, tweets["statuses"])

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

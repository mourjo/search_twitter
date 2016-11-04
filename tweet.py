#! /usr/bin/env python
import twitter
from util import is_retweet_with_hashtag
from functools import partial
import logging


class TwitterClient:
    def __init__(self,
                 consumer_key=None,
                 consumer_secret=None,
                 token=None,
                 token_secret=None):
        "Instantiate the client with the access keys."
        if all([consumer_key, consumer_secret, token, token_secret]):
            auth = twitter.OAuth(consumer_key=consumer_key,
                                 consumer_secret=consumer_secret,
                                 token=token,
                                 token_secret=token_secret)
            self.conn = twitter.Twitter(auth=auth)
        else:
            raise AttributeError("Invalid Credentials.")

    def __remove_bad_tweets(self, tweets, hashtag):
        "Remove unretweeted tweets and tweets not containing the hashtag.\
        (For some reason the search API does not always return\
        correct results.)"
        return filter(partial(is_retweet_with_hashtag, hashtag),
                      tweets["statuses"])

    def fetch_retweets_with_hashtag(self, hashtag, num=100):
        "Search retweets from using the Twitter REST API which have a hashtag."
        try:
            # Ensure there is a leading # in the hashtag.
            hashtag = hashtag if hashtag.startswith("#") else "#" + hashtag

            # Use Twitter search query to get the required tweets:
            search_query = hashtag.lower() + " min_retweets:1"

            # Call Twitter's REST API (not streaming API) to get
            # a mixed set of results (both popular and recent tweets):
            # See: https://dev.twitter.com/rest/reference/get/search/tweets
            tweets = self.conn.search.tweets(q=search_query,
                                             include_entities=True,
                                             count=num,
                                             result_type="mixed")

            tweets_with_hashtags = self.__remove_bad_tweets(tweets,
                                                            hashtag[1:])
            return tweets_with_hashtags

        except twitter.TwitterHTTPError:
            # Don't want the UI to show any error if the creds are wrong.
            # Rationale: Since this pre-authenticated server,
            # the authentication happens without the user's knowledge,
            # hence if there is a problem in oauth, the user should
            # now know of it. Showing empty results to the user instead.
            # Log the error.
            logging.warning("Could not fetch tweets from Twitter " +
                            "-- please check your credentials.")
        return []

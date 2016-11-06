from nose.tools import *
from src import tweet
from src import util


@raises(AttributeError)
def test_initialization_twitter_client():
    creds = {}
    twitter_client = tweet.TwitterClient(**creds)


def test_twitter_fetch_data():
    creds = util.fetch_credentials("src/credentials_example.json")
    twitter_client = tweet.TwitterClient(**creds)
    tweets = twitter_client.fetch_retweets_with_hashtag("custserv")
    assert_equals(tweets, [])

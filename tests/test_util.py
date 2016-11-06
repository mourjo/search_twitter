from nose.tools import *
from src import util
import os


def test_is_retweet_with_hashtag_1():
    assert_true(util.is_retweet_with_hashtag("custserv",
                                             {"retweet_count": 10,
                                              "entities": {"hashtags":
                                                           [{"text": "custserv"},
                                                            {"text": "rubbish"}]}}))
    assert_false(util.is_retweet_with_hashtag("custserv",
                                              {"retweet_count": 0,
                                               "entities": {"hashtags":
                                                            [{"text": "custserv"},
                                                             {"text": "rubbish"}]}}))


@raises(KeyError)
def test_is_retweet_with_hashtag_2():
    util.is_retweet_with_hashtag("custserv",
                                 {"entities": {"hashtags":
                                               [{"text": "custserv"},
                                                {"text": "rubbish"}]}})


@raises(KeyError)
def test_is_retweet_with_hashtag_3():
    util.is_retweet_with_hashtag("custserv", {})


@raises(IOError)
def test_fetch_credentials_1():
    util.fetch_credentials("foobar.txt")


def test_fetch_credentials_2():
    path = os.path.abspath("src/credentials_example.json")
    assert_equals(util.fetch_credentials(path),
                  {"consumer_key" : "consumer_key",
                   "consumer_secret" : "consumer_secret",
                   "token" : "token",
                   "token_secret" : "token_secret"})


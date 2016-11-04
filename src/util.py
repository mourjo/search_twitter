#! /usr/bin/env python
import json


def fetch_credentials(file_name="credentials.json"):
    "Read credentials to use when querying the Twitter API."
    with open(file_name) as credentials:
        return json.load(credentials)


def is_retweet_with_hashtag(hashtag, tweet):
    "Check if a tweet is valid, ie has the hashtag and is a retweet."
    return (tweet["retweet_count"] > 0
            and
            any(htag["text"].lower() == hashtag
                for htag in tweet["entities"]["hashtags"]))

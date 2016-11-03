#! /usr/bin/env python
from tweet import TwitterClient
import util
from wsgiref.simple_server import make_server
from template import render_html_page


def application(environ, start_response):
    tweets = twitter_client.fetch_retweets_with_hashtag("custserv", 50)
    html_page = render_html_page(tweets)
    response_headers = [('Content-Type', 'text/html')]
    start_response('200 OK', response_headers)
    return html_page


def main():
    global twitter_client
    creds = util.fetch_credentials("credentials.json")
    twitter_client = TwitterClient(**creds)

    httpd = make_server('0.0.0.0', 8080, application)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "Bye!"


if __name__ == '__main__':
    twitter_client = None
    main()

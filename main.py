#! /usr/bin/env python
from tweet import TwitterClient
import util
from wsgiref.simple_server import make_server
from template import render_html_page
from cgi import parse_qs, escape


def application(environ, start_response):
    "The main server application using WSGI."
    get_params = parse_qs(environ['QUERY_STRING'])
    try:
        num = int(escape(get_params.get('num', [''])[0]))
    except ValueError:
        num = 25
    tweets = twitter_client.fetch_retweets_with_hashtag("custserv",
                                                        num+25)[0:num]
    num = len(tweets)
    html_page = render_html_page(tweets, num)
    response_headers = [('Content-Type', 'text/html')]
    start_response('200 OK', response_headers)
    return html_page


def main():
    "Entry point: Setup the environment and start the server."
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

#! /usr/bin/env python
from tweet import TwitterClient
import util
import logging
from wsgiref.simple_server import make_server
from template import render_html_page
from cgi import parse_qs, escape


def application(environ, start_response):
    "The main server application using WSGI."
    get_params = parse_qs(environ['QUERY_STRING'])
    try:
        num = abs(int(escape(get_params.get('num', [''])[0])))
    except ValueError:
        num = 25

    # Fetch some extra tweets because some tweets will not conform
    # to the search query (wonder why?)
    tweets = twitter_client.fetch_retweets_with_hashtag("custserv",
                                                        num+25)[0:num]

    # Recalculate num so that the UI shows exactly the number of tweets
    # that conform to the search query
    num = len(tweets)

    html_page = render_html_page(tweets, num)
    response_headers = [('Content-Type', 'text/html')]
    start_response('200 OK', response_headers)

    return html_page


def main():
    "Entry point: Setup the environment and start the server."
    global twitter_client

    try:
        # The credentials file must exist,
        # see credentials_example.json for reference.
        # https://dev.twitter.com/oauth/overview/single-user
        # (Why single user auth? See readme.md.)
        creds = util.fetch_credentials("src/credentials.json")
        twitter_client = TwitterClient(**creds)

        # Port 80 requires root access -- use Nginx to
        # route traffic from 80 to 8080 instead.
        # Allow only traffic coming in via Nginx
        # (ie only from localhost and not 0.0.0.0).
        httpd = make_server('localhost', 8080, application)

        httpd.serve_forever()

    except AttributeError:
        logging.warning("Invalid credentials, cannot start server.")

    except IOError:
        logging.warning("Credentials file does not exist, " +
                        "cannot start server.")

    except KeyboardInterrupt:
        print "Bye!"


if __name__ == '__main__':
    twitter_client = None
    main()

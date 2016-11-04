# Kayako take-home task

Write a simple Twitter API client in Python. This client simply has to
fetch and display Tweets that
* Have been re-tweeted at least once
* Contain the hashtag `#custserv`


## Requirements
1. **Plan well.** The goal here is not to finish the task as quickly
   as possible, but to demonstrate your careful thinking and planning.
2. **Write for the future.** Write your code as if someone else will
   be working with it the next day. That person should be able to hit
   the ground running immediately.
3. **OOP.** You don't have to over-engineer this, but we do expect
   your small app to be object oriented.
4. **Craft your code.** At Kayako, we write beautiful code. A big part
   of code beauty is readability and reusability, which is made up of
   simple stuff like spacing, layout and consistency.
5. **Keep dependencies to a minimum.** Importing a twitter
   SDK/API-client would be sensible for this task, but using a
   full-featured web framework would probably be overkill.
6. **Publicly accessible.** Present the solution as a publicly
   accessible URL.



## Running the server
To run the server locally, two things are necessary:
1. Install dependencies using `pip install -r
   requirements.txt`. Preferable to use `virtualenv`.
2. Obtaining access tokens to pre-authenticate the server so as to be
   able to access Twitter APIs. The obtained tokens shoud be placed in
   a file named `src/credentials.json` (the file does not exist by
   default). See `credentials_example.json` for the example
   format. See the Twitter docs on how to obtain the tokens
   [here](https://dev.twitter.com/oauth/overview/application-owner-access-tokens).
3. Run the server using: `python src/main.py`. The server will listen
   on `localhost:8080`.
4. [Optional] Start Nginx with the following basic config to serve
requests to port 80:
```
server {
   listen          80;
   server_name     <server_name>;
   location / {
      proxy_pass   http://0.0.0.0:8080; # forward to python server on port 80
   }
}
```

### Publicly accessible
* There is a publicly accessible instance running at
  [`http://scratch.mourjo.me`](http://scratch.mourjo.me).
* The code is publicly available at
  [https://github.com/mourjo/search_twitter](https://github.com/mourjo/search_twitter).




## Basic architecture
* A simple
  [WSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface)
  Python server that does only one thing -- returns retweets with
  `#custserv`.
* The server runs on port `8080` and accepts requests from `localhost`
  only.
* [Nginx](https://www.nginx.com/resources/wiki/) should be used to
  route traffic from port 80 to the Python Server from the rest of the
  world.
* The live version of the server is hosted on `Amazon EC2` with Nginx
  and requests follow the following flow:

```
 +---------------------+
 |                     |
 |       Client        |<----+
 |                     |     |
 +---------------------+     |
           |                 |
           |                 |
           V                 |
 +---------------------+     |
 |                     |     |
 |   Nginx (Port 80)   |     |
 |                     |     |
 +---------------------+     |
           |                 |
           |                 |
           V                 |
 +---------------------+     |
 |                     |-----+
 |    Python Server    |
 |     (Port 8080)     |<----+
 +---------------------+     |
           |                 |
           |                 |
           V                 |
 +---------------------+     |
 |                     |     |
 |  Twitter REST API   +-----+
 |                     |
 +---------------------+
```


## Design choices

### Why single-user authentication?
The server relies on pre-authenticated tokens obtained with
[single-user OAuth](https://dev.twitter.com/oauth/overview/single-user). This
means that the server needs access on behalf of a user -- the
alternative would be to use
[3-legged authentication](https://dev.twitter.com/oauth/3-legged) but
it was not used here to keep the server as simple as possible (the
problem statement asks to make a `simple` Twitter client). Using
3-legged authentication would require the server to support multiple
routes -- that would be cumbersome to do without using a Web
development framework like `Flask` or `Django` (but the requirement
was to use minimal dependencies).

### OOP
The server uses a class `TwitterClient` to fetch tweets using the
Twitter REST API. Other things like, rendering the HTML, utility
functions are not kept inside a class because it is not
necessary. Only things that need to be instantiated are done using
Objects -- like the `TwitterClient` which is instantiated with
credentials. Having classes and using its static functions only makes
no sense in a language like Python which allows functions to be top
level entities.

### Dependencies
One of the requirements of the project was to use minimal dependencies
and hence the **only dependency** is
[a Python library](https://pypi.python.org/pypi/twitter) to call the
Twitter API. The server, logging and rendering all use native Python
language constructs.

### Absence of unit tests
Unit tests are missing from this project for the lack of time.



## Notes

### Credentials
The credentials must be obtained from
[dev.twitter.com](https://dev.twitter.com) and should be placed in a
file named `src/credentials.json` in this form:
```
{"consumer_key": "consumer_key",
 "consumer_secret": "consumer_secret",
 "token": "token",
 "token_secret": "token_secret"}
```

### Filtering of search results
The Twitter search API is called to fetch tweets using Twitter's
[advanced search queries](http://www.labnol.org/internet/twitter-search-tricks/13693/). There
are often some tweets returned by Twitter which do not conform to the
query (for example, tweets which do not have retweets and/or tweets
that do not contain the hashtag we searched for). For this reason, the
search results are filtered to check for the required properties
before sending to the client.

### Code style
Most of the code in the project conforms to
[PEP8](https://www.python.org/dev/peps/pep-0008/) (the only exception
is the `src/template.py` in which lines exceed 79 characters to retain
readability of HTML).

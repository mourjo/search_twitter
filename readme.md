# Search Twitter for #tag

A simple Twitter API client in Python which simply fetches and 
displays retweets that contain a hastag.


## Running the server
To run the server locally, two things are necessary:

1. Install dependencies using `make init`. Preferable to use `virtualenv`.
2. Obtaining access tokens to pre-authenticate the server so as to be
   able to access Twitter APIs. The obtained tokens shoud be placed in
   a file named `src/credentials.json` (the file does not exist by
   default). See `credentials_example.json` for the example
   format. See the Twitter docs on how to obtain the tokens
   [here](https://dev.twitter.com/oauth/overview/application-owner-access-tokens).
3. Run the server using: `make run`. The server will listen
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

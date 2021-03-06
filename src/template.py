#! /usr/bin/env python
def get_html_tweet(tweet):
    "Convert a tweet dictionary to an HTML blockquote."
    # Construct the Twitter status URL and put it in a <a> tag
    # and let Twitter's Javascript load the full tweet at the
    # client side.
    return tweet_template % {"tweet_text": tweet["text"],
                             "screen_name": tweet["user"]["screen_name"],
                             "tweet_id": tweet["id_str"]}


def render_html_page(tweet_objects, num, hashtag):
    "Render the full html page with tweets as blockquotes."
    # Convert the tweets individually to html
    tweet_htmls = map(get_html_tweet, tweet_objects)

    # Wrap the tweets in their own div
    rendered_tweets = '</div>\n\n<div>'.join(tweet_htmls).encode('utf-8')

    # Display the number of tweets to be fetched depending on the previous
    # request -- by default, only show 25, 50, 75.
    select_options = []
    found = False
    for i in [25, 50, 75]:
        if i == num:
            found = True
            select_options.append('<option selected="selected"> %s </option>'
                                  % str(i))
        else:
            select_options.append('<option> %s </option>' % str(i))

    # If the number was entered manually, the dropdown should show
    # the correct number of tweets.
    if not found:
        select_options.append('<option selected="selected"> %s </option>'
                              % str(num))

    # Why is the response a list?
    # PEP333: When called by the server, the application object must return an
    # iterable yielding zero or more strings.
    # https://www.python.org/dev/peps/pep-0333/#the-start-response-callable
    full_page_html = [(page_template % {"options": '\n'.join(select_options),
                                        "tweets": rendered_tweets,
                                        "hashtag" : hashtag})]

    return full_page_html


tweet_template = '''<blockquote class="twitter-tweet tw-align-center">
                         %(tweet_text)s
                        <br/>
                        <a href="https://twitter.com/%(screen_name)s/status/%(tweet_id)s">
                            https://twitter.com/%(screen_name)s/status/%(tweet_id)s
                        </a>
                    </blockquote>'''


# Reuse html layout from http://mourjo.me
page_template = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="Personal Webpage">
        <meta name="author" content="Mourjo Sen">
        <meta name="robots" content="all" />
        <link rel="shortcut icon" href="http://mourjo.me/assets/ico/favicon.png">
        <title>Mourjo Sen | Scratch </title>
        <link href="http://mourjo.me/assets/css/bootstrap.min.css" rel="stylesheet">
        <link href="http://mourjo.me/assets/css/layout.css" rel="stylesheet">
        <link href="http://mourjo.me/assets/font-awesome-4.6.3/css/font-awesome.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css?family=Unica+One|Roboto+Condensed:300,400" rel="stylesheet">
        <script src="http://mourjo.me/assets/js/ie-emulation-modes-warning.js"></script>
        <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
        <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
        <![endif]-->
        <meta name="description" content="Page description." />
        <!-- Open Graph data-->
        <meta property="og:title" content="Mourjo Sen" />
        <meta property="og:type" content="article" />
        <meta property="og:url" content=" http://mourjo.github.io/" />
        <meta property="og:image" content="http://mourjo.me/assets/img/me11.jpg" />
        <meta property="og:description" content="This is the personal page of Mourjo Sen." />
        <meta property="og:site_name" content="Personal site of Mourjo Sen" />
        <meta property="fb:admins" content="Facebook numeric ID" />
        <!--Twitter Card data-->
        <meta name="twitter:card" content="summary"/>
        <meta name="twitter:site" content="@mourjo_sen"/>
        <meta name="twitter:title" content="Mourjo Sen"/>
        <meta name="twitter:description" content="This is the personal page of Mourjo Sen."/>
        <meta name="twitter:creator" content="@mourjo_sen"/>
        <!--Twitter Summary card images must be at least 200x200px-->
        <meta name="twitter:image" content="http://mourjo.me/assets/img/me_tw.jpg"/>
    </head>
    <body>
        <div class="site-wrapper">
            <div class="site-wrapper-inner">
                <div class="cover-container">
                    <div class="masthead clearfix">
                        <div class="inner">
                            <!-- Unica one -->
                            <h3 class="masthead-brand"><a href="http://mourjo.me/index.html">MOURJO SEN</a></h3>
                            <nav>
                                <ul class="nav masthead-nav">
                                    <li ><a href="http://mourjo.me/index.html">Home</a></li>
                                    <li ><a href="http://mourjo.me/aboutme.html">About me</a></li>
                                    <li ><a href="http://mourjo.me/education.html">Education</a></li>
                                    <li ><a href="http://mourjo.me/projects.html">Projects</a></li>
                                    <li ><a href="http://mourjo.me/skills.html">Skills</a></li>
                                    <li ><a href="http://mourjo.me/cv.html">CV</a></li>
                                </ul>
                            </nav>
                        </div>
                    </div>
                    <div class="inner cover" style="padding-top: 0px;">
                        <div class="col-md-12" style="vertical-align: middle; text-align: center; ">
                            <form method="get" action="">
                                <h2 style="margin-top:0px">Retweeted tweets containing
                                    <input name="hashtag" type="text" autocomplete="off" value="%(hashtag)s" autofocus="autofocus" id="hashtag" style="background-color: #2d5886; color:white; border-radius: 50px; outline: none; text-align:center; border:2px solid white; max-width:190px" onsubmit="this.form.submit();"/>
                                </h2>
                                <div class="form-inline" style="padding-bottom: 30px; font-size: 15px">
                                    <i> Showing &nbsp; </i>
                                    <select class="dropdown-toggle" name="num" style="background-color:#1D3956;" onchange="this.form.submit();">
                                        %(options)s
                                    </select>
                                    <i>&nbsp; tweets that were retweeted at least once</i>
                                </div>
                            </form>
                        </div>
                        <div class="col-md-12" style="vertical-align: middle; text-align: center;">
                        <div>%(tweets)s</div>
                        </div>
                    </div>
                    <div class="mastfoot">
                        <div class="inner">
                            <p><i class="fa fa-copyright" aria-hidden="true"></i> Mourjo Sen 2016</p>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
    <script src="http://mourjo.me/assets/js/jquery-1.11.2.min.js"></script>
    <script src="http://mourjo.me/assets/js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="http://mourjo.me/assets/js/ie10-viewport-bug-workaround.js"></script>
    <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
</body>
</html>
'''

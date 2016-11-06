from nose.tools import *
from src import template


def test_get_html_tweet():
    expected = '''<blockquote class="twitter-tweet tw-align-center">
                         sometext
                        <br/>
                        <a href="https://twitter.com/mourjo/status/123">
                            https://twitter.com/mourjo/status/123
                        </a>
                    </blockquote>'''
    actual = template.get_html_tweet({"text": "sometext",
                                      "user": {"screen_name": "mourjo"},
                                      "id_str": "123"})
    assert_equals(expected, actual)


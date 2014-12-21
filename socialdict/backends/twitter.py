"""
Twitter backend.
"""

from datetime import datetime

import requests
from requests_oauthlib import OAuth1

from django.conf import settings

from socialdict.backends import common


SEARCH_URL = 'http://search.twitter.com/search.json' %\
             { 'hashtag': settings.SOCIALDICT_HASHTAG }
API_BASE = 'https://api.twitter.com/1.1/'
auth_url = API_BASE + 'account/verify_credentials.json'
tweets_url = API_BASE + 'search/tweets.json'

tweets_params = {
    'q': '#%s' % settings.SOCIALDICT_HASHTAG,
    'count': 100,
}

DATETIME_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'
SOURCE = 'twitter'


def update_database_terms():
    """Reads the Twitter API response and passes the necessary data
       to add terms to the database.
    """
    status = []

    auth = OAuth1(settings.TWITTER_APP_KEY,
                  settings.TWITTER_APP_SECRET,
                  settings.TWITTER_USER_OAUTH_TOKEN,
                  settings.TWITTER_USER_OAUTH_TOKEN_SECRET)
    requests.get(auth_url, auth=auth)
    response = requests.get(tweets_url, auth=auth, params=tweets_params)
    for result in response.json()['statuses']:
        # Try to match a valid datetime object
        try:
            created = datetime.strptime(result['created_at'], DATETIME_FORMAT)
        except ValueError:
            created = None
        st = common.add_term(result['text'], result['user']['screen_name'],
                             result['id'], created, SOURCE)
        status.append(st)
    return status


def build_url(user, id):
    """Creates a valid Twitter message URL based on the user id and the
       status_id of the message.
    """
    return "http://twitter.com/%s/status/%s" % (user, id)

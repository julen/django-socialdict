"""
Twitter backend.
"""

from datetime import datetime

from django.conf import settings

from socialdict.backends import common
from socialdict.models import Term

MODULE_NAME = 'Twitter'
SEARCH_URL = 'http://search.twitter.com/search.json?rpp=100&q=%%23%(hashtag)s' %\
             { 'hashtag': settings.SOCIALDICT_HASHTAG }
DATETIME_FORMAT = '%a, %d %b %Y %H:%M:%S +0000'

def update_database_terms():
    """Reads the Twitter API response and passes the necessary data
       to add terms to the database.
    """
    status = []
    response = common.load_json_response(SEARCH_URL)
    for result in response['results']:
        # Try to match a valid datetime object
        try:
            created = datetime.strptime(result['created_at'], DATETIME_FORMAT)
        except ValueError:
            created = None
        st = common.add_term(result['text'], result['from_user'],
                             result['id'], created, Term.TWITTER_SOURCE)
        status.append(st)
    return status

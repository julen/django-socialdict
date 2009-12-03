"""
Identi.ca backend.
"""

from datetime import datetime

from django.conf import settings

from socialdict.backends import common

SEARCH_URL = 'http://identi.ca/api/search.json?rpp=100&q=%%23%(hashtag)s' %\
             { 'hashtag': settings.SOCIALDICT_HASHTAG }
DATETIME_FORMAT = '%a, %d %b %Y %H:%M:%S +0000'
SOURCE = 'identica'

def update_database_terms():
    """Reads the Identi.ca API response and passes the necessary data
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
                             result['id'], created, SOURCE)
        status.append(st)
    return status

def build_url(user, id):
    """Creates a valid Identi.ca message URL based on the status_id
       of the message.
    """
    return "http://identi.ca/notice/%s" % (id)

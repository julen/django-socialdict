"""
Update term objects by querying Twitter search methods.
"""

import os
import optparse
import sys
import urllib2

from datetime import datetime

from django.conf import settings
from django.utils import simplejson
from django.utils.safestring import mark_safe


DATETIME_FORMAT = '%a, %d %b %Y %H:%M:%S +0000'


def update_terms(verbose=False):
    from socialdict.models import Term
    from socialdict.utils import parse

    search = urllib2.urlopen('%s%s' % (settings.SOCIAL_URL,
                                       settings.SOCIAL_HASHTAG))
    response = simplejson.loads(search.read())
    for result in response['results']:
        # Try parsing text
        try:
            (term, meaning) = parse(result['text'])
            author = result['from_user']
            status_id = result['id']
            created_at = result['created_at']
            try:
                # Only add if it doesn't exist
                if Term.objects.get(status_id=status_id):
                    if verbose:
                        print "Not adding: '%s'" % term
                    continue
            except Term.DoesNotExist:
                new_term = Term()
                new_term.name = term
                new_term.meaning = mark_safe(meaning)
                new_term.social_user = author
                new_term.status_id = status_id
                # Try to match a valid datetime object
                try:
                    created = datetime.strptime(created_at, DATETIME_FORMAT)
                    new_term.date_added = created
                except ValueError:
                    pass
                new_term.save()
                if verbose:
                    print "Added: '%s'" % term
        except:
            pass

def main(argv):
    parser = optparse.OptionParser()
    parser.add_option('--settings')
    parser.add_option('-v', '--verbose', action="store_true")
    options, args = parser.parse_args(argv)
    if options.settings:
        os.environ["DJANGO_SETTINGS_MODULE"] = options.settings
    update_terms(options.verbose)

if __name__ == '__main__':
    main(sys.argv)

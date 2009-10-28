"""
Update term objects by querying Twitter search methods.
"""

import datetime
import os
import optparse
import sys
import time
import urllib2

from django.conf import settings
from django.utils import simplejson


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
            try:
                # Only add if it doesn't exist
                if Term.objects.get(status_id=status_id):
                    if verbose:
                        print "Not adding: '%s'" % term
                    continue
            except Term.DoesNotExist:
                new_term = Term()
                new_term.name = term
                new_term.meaning = meaning
                new_term.social_user = author
                new_term.status_id = status_id
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

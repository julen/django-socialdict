"""
Update term objects by querying Twitter search methods.
"""

import os
import optparse
import sys

from django.conf import settings


def print_status(status):
    """Outputs the added/not added terms."""
    for success, term in status:
        if success:
            print "Added: %s" % term
        else:
            if term:
                print "Not added: %s" % term

def update_terms(verbose=False):
    """Calls the backends to actually update the database terms."""
    for be in settings.SOCIALDICT_BACKENDS:
        try:
            backends = __import__('socialdict.backends', fromlist=[be])
            backend = getattr(backends, be)
            status = backend.update_database_terms()
            if verbose:
                print "\nStatus for %s" % backend.MODULE_NAME
                print_status(status)
        except ImportError, e:
            print e
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

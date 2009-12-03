"""
Common code useful for backends.
"""

from urllib2 import urlopen

from django.utils import simplejson

from socialdict.utils import parse
from socialdict.models import Term

def load_json_response(url):
    """Loads the given URL and returns the JSON response."""
    search = urlopen(url)
    return simplejson.loads(search.read())

def add_term(text, author, id, date, source):
    """Given the necessary data for a term, tries to check for
       existing terms to avoid duplicates, and if none is found,
       it is added to the database.
    """
    def term_exists(status_id, source, term, meaning):
        """Checks if a definition with the given data exists."""
        try:
            Term.objects.get(status_id=status_id, source=source)
            return True
        except Term.DoesNotExist:
            try:
                Term.objects.get(name__iexact=term, meaning__icontains=meaning)
                return True
            except Term.DoesNotExist:
                return False

    try:
        term, meaning = parse(text)
        # Only add term if it doesn't exist
        if not term_exists(id, source, term, meaning):
            new_term = Term()
            new_term.name = term
            new_term.meaning = meaning
            new_term.social_user = author
            new_term.status_id = id
            new_term.source = source
            new_term.save()
            return True, term
        else:
            return False, term
    except:
        return False, None

import re

from django.conf import settings

reURL = re.compile("([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)[-A-Za-z0-9]*\\.)[-A-Za-z0-9\\.]+)(:[0-9]*)?")
hashtag = "#%s" % settings.SOCIAL_HASHTAG
reHASH = re.compile(hashtag, re.IGNORECASE)

def parse(text):
    """
    Parses the given text into term and meaning.
    """
    # Remove hashtag and trailing whitespaces
    clean_text = reHASH.sub("", text).strip()
    # We discard those entries with URLs inside
    if reURL.search(clean_text):
        raise
    parts = clean_text.split(':')
    if len(parts) != 2:
        raise
    term = parts[0].strip().lower()
    meaning = parts[1].strip().capitalize()
    return (term, meaning)

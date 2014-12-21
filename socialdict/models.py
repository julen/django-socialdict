import datetime

from django.db import models
from django.utils.translation import ugettext as _

class Term(models.Model):
    WEB_SOURCE = "web"

    name = models.CharField(max_length=50, verbose_name=_("Term"))
    meaning = models.CharField(max_length=140, verbose_name=_("Meaning"))
    status_id = models.IntegerField(blank=True)
    alphabet_letter = models.CharField(max_length=1, blank=True)
    social_user = models.CharField(max_length=50, blank=True, verbose_name=_("User"))
    date_added = models.DateTimeField(default=datetime.datetime.now)
    source = models.CharField(max_length=50, default=WEB_SOURCE)

    def __unicode__(self):
        return self.name

    def save(self):
        normalized_name = self.name.lower()
        self.name = normalized_name
        i = 0
        while not normalized_name[i].isalpha():
            i += 1
        self.alphabet_letter = normalized_name[i]

        super(Term, self).save()

    def get_term_url(self):
        if self.source == self.WEB_SOURCE:
            return ''

        backends = __import__('socialdict.backends', fromlist=[str(self.source)])
        backend = getattr(backends, self.source)
        return backend.build_url(self.social_user, self.status_id)

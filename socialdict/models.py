import datetime

from django.db import models
from django.utils.translation import ugettext as _

class Term(models.Model):
    WEB_SOURCE = 1
    IDENTICA_SOURCE = 2
    TWITTER_SOURCE = 3
    SOURCE_CHOICES = (
        (WEB_SOURCE, _('Web')),
        (IDENTICA_SOURCE, _('Identi.ca')),
        (TWITTER_SOURCE, _('Twitter')),
    )

    name = models.CharField(max_length=50, verbose_name=_("Term"))
    meaning = models.CharField(max_length=140, verbose_name=_("Meaning"))
    status_id = models.IntegerField(blank=True)
    alphabet_letter = models.CharField(max_length=1, blank=True)
    social_user = models.CharField(max_length=50, blank=True, verbose_name=_("User"))
    date_added = models.DateTimeField(default=datetime.datetime.now)
    source = models.IntegerField(choices=SOURCE_CHOICES, default=WEB_SOURCE)

    def __unicode__(self):
        return self.name

    def save(self):
        normalized_name = self.name.lower()
        self.name = normalized_name
        self.alphabet_letter = normalized_name[0]
        if not self.meaning.endswith(('.', '!', '?')):
            self.meaning = self.meaning + u'.'
        super(Term, self).save()

import datetime

from django.db import models
from django.utils.translation import ugettext as _

class Term(models.Model):
    name = models.CharField(max_length=30, primary_key=True, unique=True,
                            verbose_name=_("Term"))
    meaning = models.CharField(max_length=140, verbose_name=_("Meaning"))
    status_id = models.IntegerField()
    alphabet_letter = models.CharField(max_length=1, blank=True)
    social_user = models.CharField(max_length=30, blank=True, verbose_name=_("User"))
    date_added = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.name

    def save(self):
        normalized_name = self.name.lower()
        self.name = normalized_name
        self.alphabet_letter = normalized_name[0]
        if not self.meaning.endswith('.'):
            self.meaning = self.meaning + u'.'
        super(Term, self).save()

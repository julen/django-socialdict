from django.conf.urls import patterns, url

from socialdict.models import Term 
from socialdict.views import LetterView


urlpatterns = patterns('',
    url(r'^(?P<letter>\w)/(?P<page>[0-9]+)/?$',
        LetterView.as_view(),
        name='socialdict_letter_view_page'),
    url(r'^(?P<letter>\w)/?$',
        LetterView.as_view(),
        name='socialdict_letter_view'),

    #url(r'^add/?$',
    #    'socialdict.views.add',
    #    name='socialdict_add_term'),
)

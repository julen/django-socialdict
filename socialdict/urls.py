from django.conf.urls.defaults import *

from socialdict.models import Term 

urlpatterns = patterns('',
    (r'^all/?$',
     'django.views.generic.list_detail.object_list',
     { 'queryset': Term.objects.all().order_by('name') },
     'socialdict_term_archive_index'),

    (r'^(?P<letter>\w)/(?P<page>[0-9]+)/?$',
     'socialdict.views.letter', {},
     'socialdict_letter_view_page'),
    (r'^(?P<letter>\w)/?$',
     'socialdict.views.letter', {'page': 1},
     'socialdict_letter_view'),

    (r'^add/?$',
     'socialdict.views.add', {},
     'socialdict_add_term'),
)

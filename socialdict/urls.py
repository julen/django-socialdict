from django.conf.urls.defaults import *

from socialdict.models import Term 

urlpatterns = patterns('',
    (r'^all/?$',
     'django.views.generic.list_detail.object_list',
     { 'queryset': Term.objects.all() },
     'socialdict_term_archive_index'),

    (r'^(?P<letter>\w)/?$',
     'socialdict.views.letter'),

    (r'^add/?$',
     'socialdict.views.add', {},
     'socialdict_add_term'),
)

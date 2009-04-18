from django.conf.urls.defaults import *
from events.models import Event

urlpatterns = patterns(
    'events.views',
    url(r'^(?P<slug>[-\w]+)/$', 'event_detail', name='event-detail'),
    url(r'^$', 'event_list', name='event-list'),
)

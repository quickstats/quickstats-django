import simplestats.views
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^location$', simplestats.views.LocationPattern.as_view(), name='location'),
)

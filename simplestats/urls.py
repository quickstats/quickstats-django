from django.conf.urls import patterns, url
from django.views.generic import TemplateView

import simplestats.views

urlpatterns = patterns(
    '',
    url(r'^location$', simplestats.views.LocationPattern.as_view(), name='location'),
    url(r'^timeline', TemplateView.as_view(template_name="location_timeline.html")),
)

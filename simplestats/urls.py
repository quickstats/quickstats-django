import simplestats.feed
from simplestats import prometheus, views

from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.WidgetList.as_view(), name='dashboard'),
    url(r'jobs/(?P<pk>.*)$', prometheus.PushGateway.as_view()),
    url(r'^chart/metrics$', prometheus.Metrics.as_view()),

    url(r'^(?P<slug>.*)/chart$', views.WidgetChart.as_view(), name='chart'),
    url(r'^(?P<slug>.*)/waypoints$', views.WidgetWaypoints.as_view(), name='waypoints'),

    url(r'metrics/job/(?P<api_key>[0-9a-fA-F]+)(/(?P<extra>.*))?$', prometheus.PushGateway.as_view()),

    url(r'movement/(?P<pk>.*).ics$', views.LocationCalendar.as_view(), name='location-calendar'),

    url(r'^feed$', simplestats.feed.LatestEntriesFeed(), name='feed'),
]

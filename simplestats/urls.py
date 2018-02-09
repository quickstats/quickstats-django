import simplestats.feed
from simplestats import prometheus, views

from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.WidgetList.as_view(), name='dashboard'),
    url(r'jobs/(?P<pk>.*)$', prometheus.PushGateway.as_view()),
    url(r'^metrics$', prometheus.Metrics.as_view()),

    url(r'^(?P<slug>.*)/countdown$', views.CountdownDetail.as_view(), name='countdown'),
    url(r'^(?P<slug>.*)/chart$', views.ChartDetail.as_view(), name='chart'),
    url(r'^(?P<slug>.*)/waypoints$', views.WaypointDetail.as_view(), name='waypoints'),
    url(r'^(?P<pk>.*).ics$', views.LocationCalendar.as_view(), name='location-calendar'),

    url(r'metrics/job/(?P<api_key>[0-9a-fA-F]+)(/(?P<extra>.*))?$', prometheus.PushGateway.as_view()),

    url(r'^feed$', simplestats.feed.LatestEntriesFeed(), name='feed'),
]

import simplestats.feed
from simplestats import prometheus, views

from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.Dashboard.as_view(), name='dashboard'),
    url(r'jobs/(?P<pk>.*)$', prometheus.PushGateway.as_view()),
    url(r'^chart/metrics$', prometheus.Metrics.as_view()),
    url(r'metrics/job/(?P<api_key>[0-9a-fA-F]+)(/(?P<extra>.*))?$', prometheus.PushGateway.as_view()),

    url(r'report/$', views.ReportList.as_view(), name='report-list'),
    url(r'report/(?P<pk>.*)$', views.ReportDetail.as_view(), name='report-detail'),

    url(r'location/$', views.LocationList.as_view(), name='location-list'),
    url(r'location/(?P<pk>.*)$', views.LocationDetail.as_view(), name='location-detail'),
    url(r'movement/(?P<pk>.*).ics$', views.LocationCalendar.as_view(), name='location-calendar'),

    url(r'^feed$', simplestats.feed.LatestEntriesFeed(), name='feed'),
]

import simplestats.feed
import simplestats.views
import simplestats.grafana

from django.conf.urls import url

urlpatterns = [
    url(r'^$', simplestats.views.Dashboard.as_view(), name='dashboard'),
    url(r'^chart/(?P<pk>.*)$', simplestats.views.ChartDetail.as_view(), name='chart'),

    url(r'report/$', simplestats.views.ReportList.as_view(), name='report-list'),
    url(r'report/(?P<pk>.*)$', simplestats.views.ReportDetail.as_view(), name='report-detail'),

    url(r'location/$', simplestats.views.LocationList.as_view(), name='location-list'),
    url(r'location/(?P<pk>.*)$', simplestats.views.LocationDetail.as_view(), name='location-detail'),
    url(r'movement/(?P<pk>.*).ics$', simplestats.views.LocationCalendar.as_view(), name='location-calendar'),

    url(r'^feed$', simplestats.feed.LatestEntriesFeed(), name='feed'),

    url(r'^grafana$', simplestats.grafana.Index.as_view()),
    url(r'^grafana/query$', simplestats.grafana.Query.as_view()),
    url(r'^grafana/search$', simplestats.grafana.Search.as_view()),
    url(r'^grafana/annotations$', simplestats.grafana.Annotations.as_view()),
]

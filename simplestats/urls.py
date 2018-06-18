from django.urls import path, re_path
from django.views.decorators.clickjacking import xframe_options_exempt

import simplestats.feed
from simplestats import prometheus, views

app_name = 'stats'
urlpatterns = [
    path('', views.WidgetList.as_view(), name='dashboard'),
    path('browse/<username>', views.WidgetList.as_view(), name='browse'),
    path('browse', views.PublicList.as_view(), name='public'),

    path('embed/<slug>', xframe_options_exempt(views.WidgetEmbed.as_view()), name='widget-embed'),

    path('<slug>/countdown', views.CountdownDetail.as_view(), name='countdown'),
    path('<slug>/waypoints', views.WaypointDetail.as_view(), name='widget-waypoints'),
    path('<slug>', views.WidgetDetail.as_view(), name='widget-detail'),

    path('<slug>.ics', views.LocationCalendar.as_view(), name='location-calendar'),

    path('jobs/<pk>', prometheus.PushGateway.as_view()),
    path('metrics', prometheus.Metrics.as_view()),
    re_path('metrics/job/(?P<api_key>[0-9a-fA-F]+)(/(?P<extra>.*))?', prometheus.PushGateway.as_view()),

    path('feed', simplestats.feed.LatestEntriesFeed(), name='feed'),
]

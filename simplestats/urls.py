import simplestats.feed
from simplestats import prometheus, views

from django.urls import path
app_name = 'stats'
urlpatterns = [
    path('', views.PublicList.as_view(), name='dashboard'),
    path('my', views.WidgetList.as_view(), name='public'),
    path('user/<username>', views.WidgetList.as_view(), name='username'),

    path('embed/<slug>', views.WidgetEmbed.as_view(), name='widget-embed'),

    path('<slug>/countdown$', views.CountdownDetail.as_view(), name='countdown'),
    path('<slug>/waypoints$', views.WaypointDetail.as_view(), name='widget-waypoints'),
    path('<slug>', views.WidgetDetail.as_view(), name='widget-detail'),

    path('<slug>.ics$', views.LocationCalendar.as_view(), name='location-calendar'),

    path('jobs/<pk>', prometheus.PushGateway.as_view()),
    path('metrics', prometheus.Metrics.as_view()),
    path('metrics/job/(?P<api_key>[0-9a-fA-F]+)(/(?P<extra>.*))?$', prometheus.PushGateway.as_view()),

    path('feed', simplestats.feed.LatestEntriesFeed(), name='feed'),
]

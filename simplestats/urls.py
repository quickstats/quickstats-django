import simplestats.feed
from simplestats import prometheus, views

from django.urls import path
from django.views.decorators.clickjacking import xframe_options_exempt

app_name = "stats"
urlpatterns = [
    path("", views.WidgetList.as_view(), name="dashboard"),
    path("browse/<username>", views.WidgetList.as_view(), name="browse"),
    path("browse", views.WidgetList.as_view(), name="public"),
    path("embed/<slug>", xframe_options_exempt(views.WidgetEmbed.as_view()), name="widget-embed"),
    path("widget/<slug>/countdown", views.CountdownDetail.as_view(), name="countdown"),
    path("widget/<slug>/waypoints", views.WaypointDetail.as_view(), name="widget-waypoints"),
    path("widget/<slug>", views.WidgetDetail.as_view(), name="widget-detail"),
    path("widget/<slug>.ics", views.LocationCalendar.as_view(), name="location-calendar"),
    path("feed", simplestats.feed.LatestEntriesFeed(), name="feed"),
]

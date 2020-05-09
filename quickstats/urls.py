from . import views

from django.urls import path

urlpatterns = [
    path("", views.PublicWidgets.as_view(), name="home"),
    path("create/widget", views.WidgetCreate.as_view(), name="widget-create"),
    path("subscription/<pk>/delete", views.SubscriptionDelete.as_view(), name="subscription-delete"),
    path("user/<username>/subscriptions", views.SubscriptionListView.as_view(), name="subscriptions"),
    path("user/<username>/widgets", views.UserWidgets.as_view(), name="widget-user"),
    # Widget Views
    path("widget", views.WidgetListView.as_view(), name="widget-list"),
    path("widget/<pk>", views.WidgetDetailView.as_view(), name="widget-detail"),
    path("widget/<pk>/comment", views.WidgetComment.as_view(), name="widget-comment"),
    path("widget/<pk>/delete", views.WidgetDelete.as_view(), name="widget-delete"),
    path("widget/<pk>/subscribe", views.WidgetSubscription.as_view(), name="widget-subscribe"),
    path("widget/<pk>/unsubscribe", views.WidgetUnsubscribe.as_view(), name="widget-unsubscribe"),
    path("widget/<pk>/update", views.WidgetUpdate.as_view(), name="widget-update"),
    path("widget/<pk>/increment", views.StreakIncrement.as_view(), name="streak-increment"),
    # Misc Views
    path("comments", views.CommentList.as_view(), name="comment-list"),
    path("waypoints", views.WaypointList.as_view(), name="waypoint-list"),
    path("samples", views.SampleList.as_view(), name="sample-list"),
    path("scrapes", views.ScrapeList.as_view(), name="scrape-list"),
    # Filtered List Views
    path("charts", views.ChartList.as_view(), name="chart-list"),
    path("countdowns", views.CountdownList.as_view(), name="countdown-list"),
    path("locations", views.LocationList.as_view(), name="location-list"),
    path("streaks", views.StreakList.as_view(), name="streak-list"),
]

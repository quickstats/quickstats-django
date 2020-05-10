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
    # Filtered List Views
    path("filter/<type>", views.FilterList.as_view(), name="widget-type"),
    # Misc Views
    path("recent/comments", views.CommentList.as_view(), name="comment-list"),
    path("recent/waypoints", views.WaypointList.as_view(), name="waypoint-list"),
    path("recent/samples", views.SampleList.as_view(), name="sample-list"),
    path("recent/scrapes", views.ScrapeList.as_view(), name="scrape-list"),
    path("recent/shares", views.ShareList.as_view(), name="share-list"),
]

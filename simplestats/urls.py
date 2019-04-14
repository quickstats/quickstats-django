from . import views

from django.urls import path

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("subscriptions", views.SubscriptionListView.as_view(), name="subscriptions"),
    path("subscription/<pk>/delete", views.SubscriptionDelete.as_view(), name="subscription-delete"),
    path("widgets/new", views.WidgetFromSeries.as_view(), name="widget-new"),
    path("widgets", views.WidgetListView.as_view(), name="widgets"),
    path("widget/<pk>/subscribe", views.WidgetSubscription.as_view(), name="widget-subscribe"),
    path("series/<pk>", views.SeriesDetailView.as_view(), name="series-detail"),
    path("series", views.SeriesListView.as_view(), name="series"),
]

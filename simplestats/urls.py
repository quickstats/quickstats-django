from . import views

from django.urls import path

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("subscriptions", views.SubscriptionListView.as_view(), name="subscriptions"),
    path("subscription/<pk>/delete", views.SubscriptionDelete.as_view(), name="subscription-delete"),
    path("widgets/new", views.WidgetFromSeries.as_view(), name="widget-new"),
    path("widget/<pk>/subscribe", views.WidgetSubscription.as_view(), name="widget-subscribe"),
    path("widget/<pk>/update", views.WidgetUpdate.as_view(), name="widget-update"),
    path("widgets", views.WidgetListView.as_view(), name="widget-list"),
    path("series/<pk>", views.SeriesDetailView.as_view(), name="series-detail"),
    path("series", views.SeriesListView.as_view(), name="series"),
]

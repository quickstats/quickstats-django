from . import views

from django.urls import path

urlpatterns = [
    path("", views.PublicWidgets.as_view(), name="home"),
    path("user/<username>", views.UserWidgets.as_view(), name="widget-user"),
    path("subscriptions", views.SubscriptionListView.as_view(), name="subscriptions"),
    path("subscription/<pk>/delete", views.SubscriptionDelete.as_view(), name="subscription-delete"),
    path("widget/<pk>/comment", views.WidgetComment.as_view(), name="widget-comment"),
    path("widget/<pk>/subscribe", views.WidgetSubscription.as_view(), name="widget-subscribe"),
    path("widget/<pk>/unsubscribe", views.WidgetUnsubscribe.as_view(), name="widget-unsubscribe"),
    path("widget/<pk>/update", views.WidgetUpdate.as_view(), name="widget-update"),
    path("widget/<pk>/delete", views.WidgetDelete.as_view(), name="widget-delete"),
    path("widget/<pk>", views.WidgetDetailView.as_view(), name="widget-detail"),
    path("widgets", views.WidgetListView.as_view(), name="widget-list"),
]

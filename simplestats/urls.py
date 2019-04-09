from . import views

from django.urls import path

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("subscriptions", views.SubscriptionListView.as_view(), name="subscriptions"),
]

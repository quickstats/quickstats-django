"""simplestats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import routers

from simplestats import rest

from django.contrib import admin
from django.urls import include, path

router = routers.DefaultRouter()
router.register("widget", rest.WidgetViewSet)
router.register("series", rest.SeriesViewSet)
router.register("comment", rest.CommentViewSet)
router.register("subscription", rest.SubscriptionViewSet)


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path("admin/", admin.site.urls),
    path("api/", include((router.urls, "api"), namespace="api")),
    path("", include(("simplestats.urls", "stats"), namespace="stats")),
    path("", include(("simplestats.prometheus", "prometheus"), namespace="prometheus")),
    path("grafana/", include(("simplestats.grafana", "grafana"), namespace="grafana")),
]

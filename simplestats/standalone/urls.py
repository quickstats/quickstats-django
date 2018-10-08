from rest_framework import routers

from simplestats import rest

from django.contrib import admin
from django.urls import include, path

router = routers.DefaultRouter(trailing_slash=False)
router.register("widget", rest.WidgetViewSet)

urlpatterns = [
    path("api/", include((router.urls, "api"))),
    path("admin/", admin.site.urls),

    path("", include("social_django.urls", "social")),
    path("", include("django.contrib.auth.urls")),
    path("", include("simplestats.prometheus.urls")),
    path("", include("simplestats.urls")),

]

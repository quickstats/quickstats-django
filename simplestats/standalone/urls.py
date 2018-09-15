from rest_framework_nested import routers
import simplestats.rest as rest

from django.contrib import admin
from django.urls import include, path


router = routers.DefaultRouter(trailing_slash=False)
router.register("widgets", rest.WidgetViewSet)

widget_router = routers.NestedSimpleRouter(router, r'widgets', lookup='widget')
widget_router.register(r'samples', rest.SampleViewSet, base_name='widget-samples')

urlpatterns = [
    path("api/", include((router.urls, "api"))),
    path("api/", include((widget_router.urls, "api"))),
    path("admin/", admin.site.urls),
    path("", include("social_django.urls", "social")),
    path("", include("django.contrib.auth.urls")),
    path("", include("simplestats.urls")),
]

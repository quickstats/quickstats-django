from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_nested import routers

import simplestats.rest as rest

from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
    #   terms_of_service="https://www.google.com/policies/terms/",
    #   contact=openapi.Contact(email="contact@snippets.local"),
    #   license=openapi.License(name="BSD License"),
   ),
   public=True,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register("widget", rest.WidgetViewSet)

widget_router = routers.NestedSimpleRouter(router, r'widget', lookup='widget')
widget_router.register(r'samples', rest.SampleViewSet, base_name='widget-samples')
widget_router.register(r'notes', rest.NoteViewSet, base_name='widget-notes')
widget_router.register(r'waypoints', rest.WaypointViewSet, base_name='widget-waypoints')


urlpatterns = [
    path("api/", include((router.urls, "api"))),
    path("api/", include((widget_router.urls))),
    path("admin/", admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    

    path("", include("social_django.urls", "social")),
    path("", include("django.contrib.auth.urls")),
    path("", include("simplestats.urls")),
]

"""quickstats URL Configuration

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

from rest_framework_nested import routers

from quickstats import rest

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

router = routers.DefaultRouter()
router.register("widget", rest.WidgetViewSet)
router.register("comment", rest.CommentViewSet)
router.register("subscription", rest.SubscriptionViewSet)

widget_router = routers.NestedSimpleRouter(router, "widget", lookup="widget")
widget_router.register("waypoints", rest.WaypointViewSet)
widget_router.register("samples", rest.SampleViewSet)

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("api/", include((router.urls, "api"), namespace="api")),
    path("api/", include((widget_router.urls, "api"), namespace="api-widget")),
    path("", include(("quickstats.urls", "stats"), namespace="stats")),
    path("", include(("quickstats.prometheus", "prometheus"), namespace="prometheus")),
    path("grafana/", include(("quickstats.grafana", "grafana"), namespace="grafana")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

try:
    import debug_toolbar
except ImportError:
    pass
else:
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))

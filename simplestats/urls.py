from django.urls import path

from . import grafana, prometheus

urlpatterns = [
    path("metrics/job/<job>", prometheus.PushGateway.as_view(), name="push"),
    path("grafana/search", grafana.Search.as_view(), name="grafana-search"),
    path("grafana/query", grafana.Query.as_view(), name="grafana-query"),
    path("grafana/annotations", grafana.Annotations.as_view(), name="grafana-annotations"),
]

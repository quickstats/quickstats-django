from django.urls import path, include
from . import prometheus

urlpatterns = [
    path("metrics/job/<job>", prometheus.PushGateway.as_view(), name="push")
    ]


import logging
from urllib.parse import urlencode
from django.urls import path
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Info,
    PlatformCollector,
    generate_latest,
)
from prometheus_client.parser import text_string_to_metric_families

from . import models, version

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils import timezone
from django.views import View

logger = logging.getLogger(__name__)

# Basic platform information
registry = CollectorRegistry()
PlatformCollector(registry=registry)
Info("my_build_version", "Description of info", registry=registry).info(
    {"version": version.__VERSION__}
)


def from_prometheus(sample):
    labels = sample[1]
    labels["__name__"] = sample[0]
    return urlencode({k: labels[k] for k in sorted(labels)})


class PushGateway(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        for family in text_string_to_metric_families(request.body.decode("utf8")):
            for sample in family.samples:
                series, created = models.Series.objects.get_or_create(
                    name=from_prometheus(sample), owner=request.user
                )
                logger.debug("%s %s", series.name, created)
                sample, updated = series.sample_set.update_or_create(
                    timestamp=timezone.now(), defaults={"value": sample[2]}
                )
                logger.debug("%s %s", sample.value, updated)

        return HttpResponse("Hello, World!")


class Metrics(View):
    def get(self, request):
        return HttpResponse(
            generate_latest(registry=registry), content_type=CONTENT_TYPE_LATEST
        )


urlpatterns = [
    path("metrics/job/<job>", PushGateway.as_view(), name="push"),
    path("metrics", Metrics.as_view(), name="metrics"),
]

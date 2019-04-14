import logging

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Info,
    PlatformCollector,
    generate_latest,
)
from prometheus_client.parser import text_string_to_metric_families

from . import models, version
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import path
from django.utils import timezone
from django.views import View

logger = logging.getLogger(__name__)

# Basic platform information
registry = CollectorRegistry()
PlatformCollector(registry=registry)
Info("my_build_version", "Description of info", registry=registry).info(
    {"version": version.__VERSION__}
)


def labels_from_sample(sample):
    labels = sample[1]
    labels["__name__"] = sample[0]
    return {k: labels[k] for k in sorted(labels)}


class PushGateway(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        push_time = timezone.now()

        for family in text_string_to_metric_families(request.body.decode("utf8")):
            for s in family.samples:
                labels = labels_from_sample(s)
                series, created = models.Series.objects.filter_labels(
                    **labels
                ).get_or_create(owner=request.user, defaults={"name": s.name})
                if created:
                    logger.debug("Created series %s", series)
                    series.label_set.bulk_create(
                        [
                            models.Label(series=series, name=k, value=v)
                            for k, v in labels.items()
                        ]
                    )

                sample = series.sample_set.create(timestamp=push_time, value=s.value)

                logger.debug("%s", sample)

        return HttpResponse("Hello, World!")


class Metrics(View):
    def get(self, request):
        return HttpResponse(
            generate_latest(registry=registry), content_type=CONTENT_TYPE_LATEST
        )


urlpatterns = [
    path("metrics/job/<job>", csrf_exempt(PushGateway.as_view()), name="push"),
    path("metrics", Metrics.as_view(), name="metrics"),
]

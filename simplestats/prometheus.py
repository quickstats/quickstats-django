import operator
import logging
from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils import timezone
from django.views import View

from prometheus_client.parser import text_string_to_metric_families

from . import models

logger = logging.getLogger(__name__)


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

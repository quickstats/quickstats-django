import logging

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Info,
    PlatformCollector,
    generate_latest,
)
from prometheus_client.parser import text_string_to_metric_families
from rest_framework.authtoken.models import Token
from django.contrib import messages
from . import models, version

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.urls import path
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

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


class PushGateway(UserPassesTestMixin, View):
    def test_func(self):
        try:
            self.token = Token.objects.get(pk=self.kwargs["token"])
            return True
        except Token.DoesNotExist:
            return False

    def post(self, request, token, **kwargs):
        push_time = timezone.now()
        response = []

        for family in text_string_to_metric_families(request.body.decode("utf8")):
            for s in family.samples:
                labels = labels_from_sample(s)
                widget, created = models.Widget.objects.filter_labels(**labels).get_or_create(
                    owner=self.token.user, defaults={"title": s.name}
                )
                if created:
                    logger.debug("Created widget %s", widget)
                    response.append("Created widget %s" % widget)
                    widget.label_set.bulk_create(
                        [models.Label(widget=widget, name=k, value=v) for k, v in labels.items()]
                    )

                sample = widget.sample_set.create(timestamp=push_time, value=s.value)
                response.append("Appended sample to %s" % widget)

                logger.debug("%s", sample)

        return HttpResponse("\n".join(response))


class Metrics(View):
    def get(self, request):
        return HttpResponse(generate_latest(registry=registry), content_type=CONTENT_TYPE_LATEST)


class Help(LoginRequiredMixin, TemplateView):

    template_name = "simplestats/prometheus/help.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["token"], created = Token.objects.get_or_create(user=self.request.user)
        if created:
            messages.success(self.request, "Created api key")
        return context


urlpatterns = [
    path("metrics/job/<token>", csrf_exempt(PushGateway.as_view()), name="push"),
    path("metrics/job", Help.as_view(), name="help"),
    path("metrics", Metrics.as_view(), name="metrics"),
]

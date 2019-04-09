import json
import logging

from dateutil.parser import parse

from . import models

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from django.urls import path


logger = logging.getLogger(__name__)


class Search(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        query = json.loads(request.body.decode("utf8"))
        logger.debug("search %s", query)
        return JsonResponse(
            [
                {"text": subscription.widget.name, "value": subscription.id}
                for subscription in models.Subscription.objects.filter(
                    owner=request.user
                ).prefetch_related("widget")
            ],
            safe=False,
        )


class Query(LoginRequiredMixin, View):
    def datapoints(self, targets, start, end):
        for target in targets:
            yield {"target": target, "datapoints": []}

    def post(self, request, **kwargs):
        query = json.loads(request.body.decode("utf8"))
        from_ = parse(query["range"]["from"])
        to_ = parse(query["range"]["to"])

        logger.debug("%s %s %s", query, from_, to_)

        return JsonResponse(
            list(self.datapoints(query["targets"], from_, to_)), safe=False
        )


class Annotations(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        query = json.loads(request.body.decode("utf8"))
        logger.debug("annotations %s", query)
        return JsonResponse({})


urlpatterns = [
    path("query", Query.as_view(), name="query"),
    path("search", Search.as_view(), name="search"),
    path("annotations", Annotations.as_view(), name="annotations"),
]

import json
import logging

from dateutil.parser import parse
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from . import models

from django.http import JsonResponse
from django.urls import path
from django.views.generic.base import TemplateView

logger = logging.getLogger(__name__)


class Home(TemplateView):

    template_name = "simplestats/grafana/home.html"


class Search(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        query = json.loads(request.body.decode("utf8"))
        logger.debug("search %s", query)
        return JsonResponse(
            [
                subscription.widget.name
                for subscription in models.Subscription.objects.filter(
                    owner=request.user
                ).prefetch_related("widget")
            ],
            safe=False,
        )

        return JsonResponse(
            [
                {"text": subscription.widget.name, "value": subscription.id}
                for subscription in models.Subscription.objects.filter(
                    owner=request.user
                ).prefetch_related("widget")
            ],
            safe=False,
        )


def to_ts(dt):
    return dt.timestamp() * 1000


class Query(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def datapoints(self, targets, start, end):
        for t in targets:
            for widget in models.Widget.objects.filter(name=t["target"]):
                yield {
                    "target": widget.name,
                    "datapoints": [
                        [s.value, to_ts(s.timestamp)]
                        for s in widget.sample_set.filter(
                            timestamp__gte=start, timestamp__lte=end
                        )
                    ],
                }

    def post(self, request, **kwargs):
        query = json.loads(request.body.decode("utf8"))
        from_ = parse(query["range"]["from"])
        to_ = parse(query["range"]["to"])

        logger.debug("%s %s %s", query, from_, to_)

        return JsonResponse(
            list(self.datapoints(query["targets"], from_, to_)), safe=False
        )


class Annotations(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def annotations(self, targets, start, end, annotation):
        for t in targets:
            for widget in models.Widget.objects.all():
                for comment in widget.comment_set.all():
                    yield {
                        "annotation": annotation,
                        "time": to_ts(comment.timestamp),
                        "title": "Comment",
                        "tags": [comment.owner.username],
                        "text": comment.body,
                    }

    def post(self, request, **kwargs):
        query = json.loads(request.body.decode("utf8"))
        from_ = parse(query["range"]["from"])
        to_ = parse(query["range"]["to"])

        logger.debug("annotations %s", query)
        return JsonResponse(
            list(self.annotations(query, from_, to_, query["annotation"])), safe=False
        )


urlpatterns = [
    # Need to have a / for grafana-json-plugin
    path("", Home.as_view(), name="home"),
    path("query", (Query.as_view()), name="query"),
    path("search", (Search.as_view()), name="search"),
    path("annotations", (Annotations.as_view()), name="annotations"),
]

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


class Help(TemplateView):

    template_name = "quickstats/grafana/help.html"


class Search(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def fetch(self, request):
        def format(widget):
            value = widget.label_set.get(name="__name__").value
            title = widget.title
            return {"value": value, "text": title + " (" + value + ")"}

        for subscription in (
            models.Subscription.objects.filter(owner=request.user)
            .filter(widget__label__name="__name__")
            .prefetch_related("widget", "widget__label_set")
        ):
            yield format(subscription.widget)

    def post(self, request, **kwargs):
        # Get all widgets that the user is subscribed to and has a
        # metric __name__ associated with
        query = json.loads(request.body.decode("utf8"))
        logger.debug("search %s", query)

        return JsonResponse(
            sorted(self.fetch(request), key=lambda k: k["value"]), safe=False
        )


def to_ts(dt):
    return dt.timestamp() * 1000


class Query(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def datapoints(self, targets, start, end):
        for t in targets:
            for widget in models.Widget.objects.filter_labels(**{"__name__": t["target"]}):
                yield {
                    "target": widget.title,
                    "datapoints": [
                        [s.value, to_ts(s.timestamp)]
                        for s in widget.sample_set.filter(timestamp__gte=start, timestamp__lte=end).order_by('timestamp')
                    ],
                }

    def post(self, request, **kwargs):
        query = json.loads(request.body.decode("utf8"))
        start = parse(query["range"]["from"])
        end = parse(query["range"]["to"])

        logger.debug("%s %s %s", query, start, end)

        return JsonResponse(list(self.datapoints(query["targets"], start, end)), safe=False)


app_name = "grafana-quickstats"

urlpatterns = [
    # Need to have a / for grafana-json-plugin
    path("", Help.as_view(), name="help"),
    path("query", (Query.as_view()), name="query"),
    path("search", (Search.as_view()), name="search"),
]


import logging

from prometheus_client import CollectorRegistry, Gauge, generate_latest
from prometheus_client.parser import text_string_to_metric_families
from rest_framework.authtoken.models import Token

from simplestats import models, shortcuts

from django.http import HttpResponse, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

logger = logging.getLogger(__name__)


class Metrics(View):
    def get_queryset(self):
        # if self.request.user.is_authenticated:
        #     return models.Widget.objects.filter(owner=self.request.user)
        return models.Widget.objects.filter(public=True)

    # TODO Temporary bridge
    def get(self, request):
        registry = CollectorRegistry()
        gauges = {}
        for chart in self.get_queryset():
            labels = {x.name: x.value for x in chart.label_set.all()}
            metric = labels.pop('metric', '').replace('.', '_')
            if not metric:
                logging.debug('Error with metric %s %s', chart, labels)
                continue
            if not metric in gauges:
                gauges[metric] = Gauge(metric, metric, labels.keys(), registry=registry)
            if labels:
                gauges[metric].labels(**labels).set(chart.value)
            else:
                gauges[metric].set(chart.value)
        return HttpResponse(generate_latest(registry), content_type="text/plain")


@method_decorator(csrf_exempt, name='dispatch')
class PushGateway(View):
    def post(self, request, api_key, extra=None):
        try:
            token = Token.objects.get(key=api_key)
        except:
            return HttpResponseForbidden('Invalid token')

        labels = {}
        if extra:
            key = None
            for t in extra.split('/'):
                if key:
                    labels[key], key = t, None
                else:
                    key = t

        for family in text_string_to_metric_families(request.body.decode('utf8')):
            for sample in family.samples:
                shortcuts.quick_record(
                    metric=sample[0],
                    labels=dict(sample[1], **labels),
                    value=sample[2],
                    owner=token.user
                )
        return HttpResponse('ok', status=202)
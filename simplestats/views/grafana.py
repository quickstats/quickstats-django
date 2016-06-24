'''
Data source for grafana

https://grafana.net/plugins/grafana-simple-json-datasource
'''
import datetime
import json

import simplestats.models as models

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class Index(View):
    def get(self, request):
        return HttpResponse('OK')


@method_decorator(csrf_exempt, name='dispatch')
class Query(View):
    def post(self, request):
        body = json.loads(request.body.decode("utf-8"))
        start = datetime.datetime.strptime(body['range']['from'], DATETIME_FORMAT)
        end = datetime.datetime.strptime(body['range']['to'], DATETIME_FORMAT)

        results = []

        for target in body['targets']:
            response = {
                'target': target['target'],
                'datapoints': []
            }

            for stat in models.Stat.objects\
                    .order_by('created')\
                    .filter(key=target['target'])\
                    .filter(created__gte=start)\
                    .filter(created__lte=end):
                # Time needs to be in milliseconds
                response['datapoints'].append([stat.value, stat.created_unix * 1000])

            results.append(response)
        return JsonResponse(results, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class Search(View):
    def post(self, request):
        return JsonResponse(list(models.Stat.objects.values_list('key', flat=True).distinct('key')), safe=False)

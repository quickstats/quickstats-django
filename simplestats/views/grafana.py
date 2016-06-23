'''
Data source for grafana

https://grafana.net/plugins/grafana-simple-json-datasource
'''
import json
import time

import simplestats.models as models

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View


class Index(View):
    def get(self, request):
        return HttpResponse('OK')


@method_decorator(csrf_exempt, name='dispatch')
class Query(View):
    def post(self, request):
        body = json.loads(request.body.decode("utf-8"))
        #logging.getLogger('django.db.backends').setLevel(logging.DEBUG)

        results = []
        for target in body['targets']:
            response = {
                'target': target['target'],
                'datapoints': []
            }

            for stat in reversed(models.Stat.objects.order_by('-created').filter(key=target['target'])[:24]):
                response['datapoints'].append([stat.value, int(time.mktime(stat.created.timetuple()))])

            print(response)

            results.append(response)
        return JsonResponse(results, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class Search(View):
    def post(self, request):
        return JsonResponse(list(models.Stat.objects.values_list('key', flat=True).distinct('key')), safe=False)

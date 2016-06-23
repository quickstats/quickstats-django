'''
Data source for grafana

https://grafana.net/plugins/grafana-simple-json-datasource
'''
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View


class Index(View):
    def get(self, request):
        return HttpResponse('OK')


@method_decorator(csrf_exempt, name='dispatch')
class Query(View):
    def post(self, request):
        return HttpResponse('OK')


@method_decorator(csrf_exempt, name='dispatch')
class Search(View):
    def post(self, request):
        return HttpResponse('OK')

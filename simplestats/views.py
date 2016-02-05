import json
import operator

import simplestats.models

from django.shortcuts import render
from django.views.generic.base import View


class SimpleView(View):
    def get(self, request):
        dataTable = []
        for stat in simplestats.models.Stat.objects.order_by('created').filter(key=self.filter_key):
            dataTable.append([stat.created.strftime("%Y-%m-%d %H:%M"), stat.value])

        return render(request, 'simplestats/chart/simple.html', {
            'dataTable': json.dumps([self.labels] + dataTable)
        })

class USDJPY(SimpleView):
    filter_key = 'currency.USD.JPY'
    labels = ['Datetime', 'JPY']


class Temperature(SimpleView):
    filter_key = 'weather.fukuoka.temperature'
    labels = ['Datetime', '°C']

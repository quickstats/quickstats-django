import json
import operator

import simplestats.models

from django.shortcuts import render
from django.views.generic.base import View


class USDJPY(View):
    def get(self, request):
        dataTable = {}
        for stat in simplestats.models.Stat.objects.order_by('-created').filter(key='currency.USD.JPY'):
            dataTable[stat.created] = stat.value

        return render(request, 'simplestats/chart/simple.html', {
            'dataTable': json.dumps([['Datetime', 'JPY']] + list(
                [(label.isoformat(), round(temperature, 2)) for (label, temperature) in sorted(dataTable.items(), key=operator.itemgetter(1), reverse=True)]
            ))
        })

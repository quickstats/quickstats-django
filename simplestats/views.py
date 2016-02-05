import collections
import datetime
import json
import operator

import simplestats.models

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View


class SimpleView(View):
    def get(self, request):
        dataTable = []
        for stat in simplestats.models.Stat.objects.order_by('created').filter(key=self.filter_key).filter(created__gte=datetime.datetime.now() - self.time_delta):
            dataTable.append([stat.created.strftime("%Y-%m-%d %H:%M"), stat.value])

        return render(request, 'simplestats/chart/simple.html', {
            'dataTable': json.dumps([[str(label) for label in self.labels]] + dataTable)
        })


class USDJPY(SimpleView):
    filter_key = 'currency.USD.JPY'
    labels = [_('Datetime'), 'JPY']
    time_delta = datetime.timedelta(days=30)


class Temperature(SimpleView):
    filter_key = 'weather.fukuoka.temperature'
    labels = [_('Datetime'), _('Temperature')]
    time_delta = datetime.timedelta(days=30)


class WaniKani(View):
    def get(self, request):
        def get_stats():
            stats = collections.defaultdict(lambda: collections.defaultdict(int))
            startdate = datetime.datetime.now() - datetime.timedelta(days=7)
            for stat in simplestats.models.Stat.objects.order_by('created').filter(key__in=['wanikani.reviews', 'wanikani.lessons']).filter(created__gte=startdate):
                stats[stat.created][stat.key] = stat.value
            for date, stat in sorted(stats.items()):
                yield [date.strftime("%Y-%m-%d %H:%M"), stat['wanikani.reviews'], stat['wanikani.lessons']]

        return render(request, 'simplestats/chart/annotation.html', {
            'dataTable': json.dumps([[str(_('Datetime')), 'Reviews', 'Lessons']] + list(get_stats()))
        })

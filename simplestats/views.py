import collections
import datetime
import json
import operator

import simplestats.models

from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
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

class SimpleBoard(View):
    def get(self, request):
        datapoints = []
        for stat in simplestats.models.Stat.objects.order_by('created').filter(key=self.filter_key).filter(created__gte=datetime.datetime.now() - self.time_delta):
            datapoints.append({'title': stat.created.strftime("%Y-%m-%d %H:%M"), 'value': stat.value})
        return JsonResponse({
            'graph': {
                'title': 'WaniKani',
                'type': 'line',
                'datasequences': [{
                    'title': self.label,
                    'datapoints': datapoints
                }]
            }
        })

class USDJPY(SimpleView):
    filter_key = 'currency.USD.JPY'
    labels = [_('Datetime'), 'JPY']
    time_delta = datetime.timedelta(days=30)

class USDJPYBoard(SimpleBoard):
    filter_key = 'currency.USD.JPY'
    label = 'USD/JPY'
    time_delta = datetime.timedelta(days=30)


class Temperature(SimpleView):
    filter_key = 'weather.fukuoka.temperature'
    labels = [_('Datetime'), _('Temperature')]
    time_delta = datetime.timedelta(days=30)

class TemperatureBoard(SimpleBoard):
    filter_key = 'weather.fukuoka.temperature'
    label =  'Temperature'
    time_delta = datetime.timedelta(days=30)


class WaniKani(View):
    def get_stats(self):
        stats = collections.defaultdict(lambda: collections.defaultdict(int))
        startdate = datetime.datetime.now() - datetime.timedelta(days=7)
        for stat in simplestats.models.Stat.objects.order_by('created').filter(key__in=['wanikani.reviews', 'wanikani.lessons']).filter(created__gte=startdate):
            stats[stat.created][stat.key] = stat.value
        for date, stat in sorted(stats.items()):
            yield [date.strftime("%Y-%m-%d %H:%M"), stat['wanikani.reviews'], stat['wanikani.lessons']]

    def get(self, request):
        return render(request, 'simplestats/chart/annotation.html', {
            'dataTable': json.dumps([[str(_('Datetime')), 'Reviews', 'Lessons']] + list(self.get_stats()))
        })


class WaniKaniBoard(WaniKani):
    def get(self, request):
        reviews = {
            'title': 'WaniKani Reviews',
            'color': 'red',
            'datapoints': []
        }
        lessons = {
            'title': 'Lessons',
            'color': 'purple',
            'datapoints': []
        }
        graph = {
            'graph': {
                'title': 'WaniKani',
                'type': 'line',
                'refreshEveryNSeconds': 120,
                # 'datasequences': [reviews, lessons]
                # Temporarily remove lessons for now
                'datasequences': [reviews]
            }
        }
        for t, r, l in self.get_stats():
            reviews['datapoints'].append({'title': t, 'value': r})
            lessons['datapoints'].append({'title': t, 'value': l})
        return JsonResponse(graph)

class Dashboard(View):
    '''
    Simple dashboard to show important views
    '''
    def get(self, request):
        def charts(request):
            for countdown in simplestats.models.Countdown.objects.all():
                yield render_to_string('simplestats/widget/countdown.html', {
                    'countdown': countdown,
                })
            for chart in simplestats.models.Chart.objects.all():
                yield render_to_string('simplestats/widget/chart.html', {
                    'chart': chart,
                })

        return render(request, 'simplestats/dashboard.html', {
            'charts': charts(request)
        })

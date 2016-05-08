import collections
import datetime
import json
import operator

import simplestats.models

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View

class RenderChart(View):
    def get(self, request, uuid):
        chart = simplestats.models.Chart.objects.get(id=uuid)
        labels = [_('Datetime'), chart.label]
        dataTable = []

        time_delta = datetime.timedelta(days=chart.get_meta('time_delta', 7))

        for stat in simplestats.models.Stat.objects.order_by('created').filter(key=chart.keys).filter(created__gte=datetime.datetime.now() - time_delta):
            dataTable.append([stat.created.strftime("%Y-%m-%d %H:%M"), stat.value])
        return render(request, 'simplestats/chart/simple.html', {
            'chart': chart,
            'dataTable': json.dumps([[str(_label) for _label in labels]] + dataTable),
            'panic_board': request.build_absolute_uri(reverse('stats:board', kwargs={'uuid': uuid})),
        })

class RenderBoard(View):
    def get(self, request, uuid):
        chart = simplestats.models.Chart.objects.get(id=uuid)
        labels = [_('Datetime'), chart.label]
        dataTable = []

        time_delta = datetime.timedelta(days=chart.get_meta('time_delta', 7))

        datapoints = []
        for stat in simplestats.models.Stat.objects.order_by('created').filter(key=chart.keys).filter(created__gte=datetime.datetime.now() - time_delta):
            datapoints.append({'title': stat.created.strftime("%Y-%m-%d %H:%M"), 'value': stat.value})
        return JsonResponse({
            'graph': {
                'title': chart.label,
                'type': 'line',
                'datasequences': [{
                    'title': chart.label,
                    'datapoints': datapoints
                }]
            }
        })

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
            'title': 'Reviews',
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


class KeysList(View):
    def get(self, request):
        return render(request, 'simplestats/keys.html', {
            'keys': simplestats.models.Stat.objects.values_list('key', flat=True).distinct('key').order_by('key')
        })


class Graph(View):
    '''Show the past 7 days for a single key'''
    def get(self, request, key):
        labels = [_('Datetime'), key]
        dataTable = []

        time_delta = datetime.timedelta(days=7)

        for stat in simplestats.models.Stat.objects.order_by('created').filter(key=key).filter(created__gte=datetime.datetime.now() - time_delta):
            dataTable.append([stat.created.strftime("%Y-%m-%d %H:%M"), stat.value])
        return render(request, 'simplestats/chart/simple.html', {
            'keys': simplestats.models.Stat.objects.values_list('key', flat=True).distinct('key').order_by('key'),
            'dataTable': json.dumps([[str(_label) for _label in labels]] + dataTable),
        })


class LatestEntriesFeed(Feed):
    title = "Dashboard"
    # TODO: Fix hard coded link
    link = '/stats/feeds/'
    description = "Updates on changes and additions to police beat central."

    def items(self):
        return simplestats.models.Countdown.objects.order_by('-created')

    def item_title(self, item):
        return item.label

    def item_description(self, item):
        return '{}\n{}'.format(item.created, item.description)

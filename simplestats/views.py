import datetime
import json

import simplestats.models

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView
from django.views.generic.base import View


class ReportDetail(LoginRequiredMixin, DetailView):
    model = simplestats.models.Report


class ReportList(LoginRequiredMixin, ListView):
    model = simplestats.models.Report
    paginate_by = 10


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


class Dashboard(View):
    '''
    Simple dashboard to show important views
    '''
    def get(self, request):
        if request.user.is_authenticated():
            countdowns = simplestats.models.Countdown.objects.filter(owner=request.user)
            charts = simplestats.models.Chart.objects.filter(owner=request.user)
        else:
            countdowns = simplestats.models.Countdown.objects.filter(public=True)
            charts = simplestats.models.Chart.objects.filter(public=True)

        def widgets(request):
            for countdown in countdowns:
                yield render_to_string('simplestats/widget/countdown.html', {
                    'countdown': countdown,
                })
            for chart in charts:
                yield render_to_string('simplestats/widget/chart.html', {
                    'chart': chart,
                })

        return render(request, 'simplestats/dashboard.html', {
            'widgets': widgets(request)
        })


class KeysList(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'simplestats/keys.html', {
            'keys': simplestats.models.Stat.unique_keys()
        })


class Graph(LoginRequiredMixin, View):
    '''Show the past 7 days for a single key'''
    def get(self, request, key):
        labels = [_('Datetime'), key]
        dataTable = []

        meta = {m.key: m.value for m in simplestats.models.StatMeta.objects.filter(chart=key)}

        meta['days'] = int(meta['days']) if 'days' in meta else 7
        meta['divide'] = float(meta['divide']) if 'divide' in meta else 1.0

        time_delta = datetime.timedelta(days=meta['days'])

        for stat in simplestats.models.Stat.objects.order_by('created').filter(key=key).filter(created__gte=datetime.datetime.now() - time_delta):
            dataTable.append([stat.created.strftime("%Y-%m-%d %H:%M"), stat.value / meta['divide']])

        return render(request, 'simplestats/chart/simple.html', {
            'dataTable': json.dumps([[str(_label) for _label in labels]] + dataTable),
            'keys': simplestats.models.Stat.objects.values_list('key', flat=True).distinct('key').order_by('key'),
            'meta': meta,
        })

import datetime
import json

import pytz
from icalendar import Calendar, Event
from prometheus_client import CollectorRegistry, Gauge, generate_latest
from rest_framework.authtoken.models import Token

import simplestats.models

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView
from django.views.generic.base import View


class ReportDetail(LoginRequiredMixin, DetailView):
    model = simplestats.models.Report


class ReportList(LoginRequiredMixin, ListView):
    model = simplestats.models.Report
    paginate_by = 10


class LocationList(LoginRequiredMixin, ListView):
    model = simplestats.models.Location
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(LocationList, self).get_context_data(**kwargs)
        context['token'], _ = Token.objects.get_or_create(user=self.request.user)
        return context


class LocationDetail(LoginRequiredMixin, DetailView):
    model = simplestats.models.Location


class LocationCalendar(View):
    def get(self, request, pk):
        # Verify token exists
        get_object_or_404(Token, pk=pk)

        now = datetime.datetime.now(pytz.utc)
        delta = datetime.timedelta(days=7)

        cal = Calendar()
        cal.add('prodid', '-//My calendar product//mxm.dk//')
        cal.add('version', '2.0')

        locations = {}
        for location in simplestats.models.Movement.objects\
                .filter(created__gte=datetime.datetime.now() - delta)\
                .order_by('created'):
            if location.state == 'entered':
                locations[location.note] = location.created
            elif location.state == 'exited':
                if location.note in locations:
                    entered = locations.pop(location.note)

                    event = Event()
                    event.add('summary', location.note)
                    event.add('dtstart', entered)
                    event.add('dtend', location.created)
                    event['uid'] = location.id
                    cal.add_component(event)

        # Check for any remaining locations that have not been 'popped'
        # and assume we're currently located there

        for label, entered in locations.items():
            event = Event()
            event.add('summary', label)
            event.add('dtstart', entered)
            event.add('dtend', now.replace(minute=0, second=0, microsecond=0))
            cal.add_component(event)

        return HttpResponse(
            content=cal.to_ical(),
            content_type='text/plain; charset=utf-8'
        )


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


class ChartDetail(LoginRequiredMixin, DetailView):
    model = simplestats.models.Chart

    def get_context_data(self, **kwargs):
        context = super(ChartDetail, self).get_context_data(**kwargs)
        chart = self.get_object()
        time_delta = datetime.timedelta(days=7)
        labels = [_('Datetime'), chart.label]
        dataTable = []

        for stat in chart.data_set.order_by('timestamp').filter(timestamp__gte=datetime.datetime.now() - time_delta):
            dataTable.append([stat.timestamp.strftime("%Y-%m-%d %H:%M"), stat.value])

        context['dataTable'] = json.dumps([[str(_label) for _label in labels]] + dataTable)
        return context


class ChartMetrics(View):
    # TODO Temporary bridge
    def get(self, request):
        registry = CollectorRegistry()
        gauges = {}
        for chart in simplestats.models.Chart.objects.filter(public=True):
            labels = chart.labels.copy()
            metric = labels.pop('__name__', chart.keys).replace('.', '_')
            if not metric in gauges:
                gauges[metric] = Gauge(metric, metric, labels.keys(), registry=registry)
            if labels:
                gauges[metric].labels(**labels).set(chart.value)
            else:
                gauges[metric].set(chart.value)
        return HttpResponse(generate_latest(registry), content_type="text/plain")

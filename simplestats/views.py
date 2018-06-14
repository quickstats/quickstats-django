import datetime

import pytz
from icalendar import Calendar, Event
from rest_framework.authtoken.models import Token

import simplestats.models

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView
from django.views.generic.base import View


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
        for location in simplestats.models.Waypoint.objects\
                .filter(timestamp__gte=datetime.datetime.now() - delta)\
                .order_by('timestamp'):
            if location.state == 'entered':
                locations[location.widget.title] = location.timestamp
            elif location.state == 'exited':
                if location.widget.title in locations:
                    entered = locations.pop(location.widget.title)

                    event = Event()
                    event.add('summary', location.description)
                    event.add('dtstart', entered)
                    event.add('dtend', location.timestamp)
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


class WidgetList(ListView):
    model = simplestats.models.Widget

    def get_queryset(self):
        if 'username' in self.kwargs:
            if self.kwargs['username'] == self.request.user.username:
                qs =  self.model.objects.filter(owner=self.request.user)
            else:
                qs = self.model.objects.filter(owner__username=self.kwargs['username'], public=True)
        else:
            qs = self.model.objects.filter(owner=self.request.user)

        return qs.order_by('-timestamp').prefetch_related('owner')


class PublicList(ListView):
    model = simplestats.models.Widget

    def get_queryset(self):
        return self.model.objects.filter(public=True)\
            .order_by('-timestamp')\
            .prefetch_related('owner')


class WidgetDetail(LoginRequiredMixin, DetailView):
    model = simplestats.models.Widget

    @cached_property
    def sample_set(self):
        return Paginator(self.object.sample_set.order_by('-timestamp'), 25).page(1)

    @cached_property
    def waypoint_set(self):
        return Paginator(self.object.waypoint_set.order_by('-timestamp'), 25).page(1)

    @cached_property
    def note_set(self):
        return Paginator(self.object.note_set.order_by('-timestamp'), 25).page(1)

    @property
    def embed(self):
        return 'simplestats/widget/{}.embed.html'.format(self.object.type)


class WidgetEmbed(DetailView):
    model = simplestats.models.Widget
    template_name = 'simplestats/widget/base.html'

    @property
    def embed(self):
        return 'simplestats/widget/{}.embed.html'.format(self.object.type)


class CountdownDetail(LoginRequiredMixin, DetailView):
    model = simplestats.models.Widget
    template_name = 'simplestats/countdown_detail.html'


class WaypointDetail(LoginRequiredMixin, DetailView):
    model = simplestats.models.Widget
    template_name = 'simplestats/waypoint_detail.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(WaypointDetail, self).get_context_data(**kwargs)

        paginator = Paginator(context['object'].waypoint_set.order_by('-timestamp'), 25)
        page = self.request.GET.get('page', 1)
        context['waypoint_set'] = paginator.page(page)

        return context

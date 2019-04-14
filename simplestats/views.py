from . import models

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView


class SeriesDetailView(LoginRequiredMixin, DetailView):

    model = models.Series


class Home(LoginRequiredMixin, ListView):

    model = models.Widget
    paginate_by = 100
    template_name = "simplestats/home.html"

    def get_queryset(self):
        return self.model.objects.filter(public=True)


class SubscriptionListView(LoginRequiredMixin, ListView):

    model = models.Subscription
    paginate_by = 100

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class SubscriptionDelete(LoginRequiredMixin, DeleteView):
    model = models.Subscription
    success_url = reverse_lazy("stats:subscriptions")


class WidgetFromSeries(LoginRequiredMixin, View):
    def post(self, request):
        widget = models.Widget.objects.create(
            owner=request.user, name="foo", description="bar"
        )
        for series_id in request.POST.get("series_id", []):
            widget.series.add(models.Series.objects.get(pk=series_id))
        sub = models.Subscription.objects.create(owner=request.user, widget=widget)
        return redirect("stats:widget-list")


class WidgetSubscription(LoginRequiredMixin, View):
    def post(self, request, pk):
        sub, created = models.Subscription.objects.get_or_create(
            owner=request.user, widget_id=pk
        )
        return redirect("stats:subscriptions")


class WidgetListView(LoginRequiredMixin, ListView):

    model = models.Widget
    paginate_by = 100

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class WidgetUpdate(UpdateView):
    model = models.Widget
    fields = ["name", "description", "public", "type"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("stats:widget-list")


class SeriesListView(LoginRequiredMixin, ListView):

    model = models.Series
    paginate_by = 100

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

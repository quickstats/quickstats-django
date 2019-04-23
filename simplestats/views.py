from . import models

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView


class PublicWidgets(LoginRequiredMixin, ListView):

    model = models.Widget
    paginate_by = 20
    template_name = "simplestats/home.html"

    def get_queryset(self):
        return self.model.objects.filter(public=True)


class UserWidgets(LoginRequiredMixin, ListView):

    model = models.Widget
    paginate_by = 20
    template_name = "simplestats/home.html"

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs["username"])
        qs = self.model.objects.filter(owner=user)
        if user == self.request.user:
            return qs
        return qs.filter(public=True)


class SubscriptionListView(LoginRequiredMixin, ListView):

    model = models.Subscription
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class SubscriptionDelete(LoginRequiredMixin, DeleteView):
    model = models.Subscription
    success_url = reverse_lazy("stats:subscriptions")


class WidgetSubscription(LoginRequiredMixin, View):
    def post(self, request, pk):
        sub, created = models.Subscription.objects.get_or_create(
            owner=request.user, widget_id=pk
        )
        messages.success(request, "Subscribed")
        if "next" in self.request.POST:
            return redirect(self.request.POST["next"])
        return redirect("stats:widget-list")


class WidgetUnsubscribe(LoginRequiredMixin, View):
    def post(self, request, pk):
        models.Subscription.objects.filter(owner=request.user, widget_id=pk).delete()
        messages.success(request, "Unsubscribed")
        if "next" in self.request.POST:
            return redirect(self.request.POST["next"])
        return redirect("stats:widget-list")


class WidgetListView(LoginRequiredMixin, ListView):

    model = models.Widget
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class WidgetDetailView(LoginRequiredMixin, DetailView):

    model = models.Widget


class WidgetUpdate(UpdateView):
    model = models.Widget
    fields = ["name", "description", "public", "type", "formatter"]
    template_name_suffix = "_update_form"


class WidgetDelete(LoginRequiredMixin, DeleteView):
    model = models.Widget
    success_url = reverse_lazy("stats:widget-list")

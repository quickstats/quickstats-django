from . import forms, models

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView


class PublicWidgets(ListView):

    model = models.Widget
    paginate_by = 20
    template_name = "quickstats/public.html"

    def get_queryset(self):
        return (
            self.model.objects.filter(public=True)
            .prefetch_related("owner")
            .filter_get(self.request.GET)
        )


class UserWidgets(ListView):

    model = models.Widget
    paginate_by = 20
    template_name = "quickstats/user.html"

    def get_queryset(self):
        qs = (
            self.model.objects.filter(owner__username=self.kwargs["username"])
            .prefetch_related("owner")
            .filter_get(self.request.GET)
        )

        if self.kwargs["username"] == self.request.user.username:
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
        sub, created = models.Subscription.objects.get_or_create(owner=request.user, widget_id=pk)
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


class WidgetComment(LoginRequiredMixin, SingleObjectMixin, View):
    model = models.Widget

    def post(self, request, pk):
        self.object = self.get_object()
        comment = self.object.comment_set.create(body=request.POST["body"], owner=self.request.user)
        messages.success(request, "Added new comment")
        return redirect(self.object.get_absolute_url())


class WidgetListView(LoginRequiredMixin, ListView):

    model = models.Widget
    paginate_by = 20

    def get_queryset(self):
        qs = self.model.objects.filter(owner=self.request.user).filter_get(self.request.GET)
        if "type" in self.request.kwargs:
            qs = qs.filter(type=self.request.kwargs["type"])
        return qs


class WidgetDetailView(LoginRequiredMixin, DetailView):

    model = models.Widget

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = forms.CommentForm()
        return context


class WidgetUpdate(LoginRequiredMixin, UpdateView):
    model = models.Widget
    fields = ["title", "description", "public", "type", "more"]
    template_name_suffix = "_update_form"


class WidgetDelete(LoginRequiredMixin, DeleteView):
    model = models.Widget
    success_url = reverse_lazy("stats:widget-list")


class WidgetCreate(CreateView):
    model = models.Widget
    fields = ["title", "description", "public", "type", "more"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CommentList(LoginRequiredMixin, ListView):
    model = models.Comment
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(widget__owner=self.request.user)


class WaypointList(LoginRequiredMixin, ListView):
    model = models.Waypoint
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(widget__owner=self.request.user)


class StreakIncrement(UserPassesTestMixin, SingleObjectMixin, View):
    model = models.Widget

    def test_func(self):
        return self.get_object().owner == self.request.user

    def post(self, request, pk):
        self.object = self.get_object()
        self.object.sample_set.create(
            value=request.POST["value"], timestamp=timezone.now()
        )
        messages.success(request, "Added new comment")
        return redirect(self.object.get_absolute_url())

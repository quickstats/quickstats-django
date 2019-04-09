from . import models

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView


class Home(TemplateView):

    template_name = "simplestats/home.html"


class SubscriptionListView(ListView):

    model = models.Subscription
    paginate_by = 100

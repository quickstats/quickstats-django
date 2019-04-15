import logging
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class SeriesQuerySet(models.QuerySet):
    def filter_labels(self, **labels):
        qs = self
        for k, v in labels.items():
            qs = qs.filter(Q(label__name=k, label__value=v))
        return qs


class Widget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)
    series = models.ManyToManyField(
        "simplestats.Series", blank=True, related_name="widget_set"
    )

    TYPE_CHART = 1
    TYPE_COUNTDOWN = 2
    TYPE_LOCATION = 3
    TYPE_STREAK = 4
    TYPE_CHOICES = (
        (TYPE_CHART, _("Chart")),
        (TYPE_COUNTDOWN, _("Countdown")),
        (TYPE_LOCATION, _("Location")),
        (TYPE_STREAK, _("Streak")),
    )

    type = models.IntegerField(choices=TYPE_CHOICES, default=TYPE_CHART)

    def get_absolute_url(self):
        return reverse("stats:widget-detail", args=(self.pk,))


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget = models.ForeignKey("simplestats.Widget", on_delete=models.CASCADE)
    timestamp = models.DateField(default=timezone.now)
    body = models.TextField(blank=True)


class Subscription(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget = models.ForeignKey("simplestats.Widget", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("owner", "widget")


class Series(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    public = models.BooleanField(default=False)
    value = models.FloatField(default=0)

    objects = SeriesQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse("stats:series-detail", args=(self.pk,))


class Label(models.Model):
    series = models.ForeignKey("simplestats.Series", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=128)

    class Meta:
        unique_together = ("series", "name")


class Sample(models.Model):
    series = models.ForeignKey("simplestats.Series", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.FloatField()

    class Meta:
        unique_together = ("series", "timestamp")

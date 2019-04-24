import datetime
import logging
import os
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class WidgetQuerySet(models.QuerySet):
    def filter_labels(self, **labels):
        qs = self
        for k, v in labels.items():
            qs = qs.filter(Q(label__name=k, label__value=v))
        return qs


def _upload_to_path(instance, filename):
    root, ext = os.path.splitext(filename)
    return "simplestats/{}/{}{}".format(
        instance.__class__.__name__, instance.pk, ext
    ).lower()


class Widget(models.Model):
    objects = WidgetQuerySet.as_manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)
    icon = models.ImageField(upload_to=_upload_to_path, blank=True)

    value = models.FloatField(default=0)
    formatter = models.CharField(max_length=128)

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

    @property
    def formatted(self):
        if self.type == self.TYPE_COUNTDOWN:
            return datetime.fromtimestamp(self.value)
        return self.value

    def get_absolute_url(self):
        return reverse("stats:widget-detail", args=(self.pk,))


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget = models.ForeignKey("simplestats.Widget", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    body = models.TextField()


class Subscription(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget = models.ForeignKey("simplestats.Widget", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("owner", "widget")


class Label(models.Model):
    widget = models.ForeignKey("simplestats.Widget", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=128)

    class Meta:
        unique_together = ("widget", "name")


class Sample(models.Model):
    widget = models.ForeignKey("simplestats.Widget", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.FloatField()

    class Meta:
        unique_together = ("widget", "timestamp")

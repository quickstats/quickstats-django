import logging
import os
import uuid

from pkg_resources import working_set

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

    def filter_get(self, params):
        qs = self
        filters = {key: params[key] for key in ["type"] if key in params}
        if filters:
            return qs.filter(**filters)
        return qs

    def lookup_or_create(self, labels, **kwargs):
        # Label aware version of get_or_create
        # We often want to filter on labels when using get_or_create, but on
        # creation, we need to make sure our new object is created with the
        # correct labels
        widget, created = self.filter_labels(**labels).get_or_create(**kwargs)
        if created:
            widget.label_set.bulk_create(
                [
                    Label(widget=widget, name=k, value=v)
                    for k, v in labels.items()
                ]
            )
        return widget, created


def _upload_to_path(instance, filename):
    root, ext = os.path.splitext(filename)
    return "quickstats/{}/{}{}".format(
        instance.__class__.__name__, instance.pk, ext
    ).lower()


class Widget(models.Model):
    objects = WidgetQuerySet.as_manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)
    icon = models.ImageField(upload_to=_upload_to_path, blank=True)
    more = models.URLField("External link", blank=True)

    value = models.FloatField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)

    type = models.CharField(
        max_length=16,
        default="chart",
        choices=[
            ("chart", _("Chart")),
            ("countdown", _("Countdown")),
            ("location", _("Location")),
            ("streak", _("Streak")),
        ],
    )

    def get_absolute_url(self):
        return reverse("stats:widget-detail", args=(self.pk,))


class Setting(models.Model):
    widget = models.ForeignKey("quickstats.Widget", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=128, blank=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget = models.ForeignKey("quickstats.Widget", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    body = models.TextField()

    class Meta:
        ordering = ("-timestamp",)


class Subscription(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget = models.ForeignKey("quickstats.Widget", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("owner", "widget")


class Label(models.Model):
    widget = models.ForeignKey("quickstats.Widget", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    value = models.CharField(max_length=128)

    class Meta:
        unique_together = ("widget", "name")


class Sample(models.Model):
    widget = models.ForeignKey("quickstats.Widget", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.FloatField()

    class Meta:
        ordering = ("-timestamp",)
        unique_together = ("widget", "timestamp")


class Waypoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    widget = models.ForeignKey("quickstats.Widget", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    body = models.TextField(blank=True)

    lat = models.FloatField()
    lon = models.FloatField()
    state = models.CharField(
        max_length=16,
        choices=(
            ("", _("Unselected")),
            ("enter", _("Entered an Area")),
            ("exit", _("Exited an Area")),
            ("waypoint", _("Waypoint")),
        ),
    )

    class Meta:
        ordering = ("-timestamp",)
        unique_together = ("widget", "timestamp")


class Scrape(models.Model):
    def drivers():
        yield from working_set.iter_entry_points("quickstats.scrape")

    TYPE_CHOICES = [(entity.name, entity.name) for entity in drivers()]

    widget = models.ForeignKey("quickstats.Widget", on_delete=models.CASCADE)
    driver = models.CharField(max_length=32, choices=TYPE_CHOICES)
    url = models.URLField()

    class Meta:
        unique_together = ("widget", "driver")


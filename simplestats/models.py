import logging
import os
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


def _upload_to_path(instance, filename):
    root, ext = os.path.splitext(filename)
    return 'simplestats/{}/{}{}'.format(
        instance.__class__.__name__, instance.pk, ext).lower()


class Widget(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('owner'), on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    icon = models.ImageField(upload_to=_upload_to_path, blank=True)
    value = models.FloatField(default=0)
    more = models.URLField(blank=True)
    type = models.CharField(max_length=32, choices=[
        ('chart', 'Chart'),
        ('countdown', 'Countdown'),
        ('location', 'Location'),
    ])

    def __str__(self):
        return 'Widget:{}:{}'.format(self.owner_id, self.slug)

    def meta(self, key, default=None):
        # Override __getitem__ as an easy way to get our meta fields for our
        # widget.
        # TODO: Add test cases
        # TODO: Add __setitem__ equivilant
        if not hasattr(self, '__meta'):
            self.__meta = {x.key: x.value for x in self.meta_set.all()}
        return self.__meta.get(key, default)


class Sample(models.Model):
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.FloatField()

    class Meta:
        unique_together = ('widget', 'timestamp')

    def __str__(self):
        return 'Sample:{}:{}'.format(self.widget_id, self.value)


class Note(models.Model):
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=64)
    description = models.TextField()


class Label(models.Model):
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=64)

    class Meta:
        unique_together = ('widget', 'name')

    def __str__(self):
        return self.name + ':' + self.value


class Meta(models.Model):
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE)
    key = models.CharField(max_length=64)
    value = models.TextField()
    output = models.BooleanField(default=False)

    class Meta:
        unique_together = ('widget', 'key')


class Waypoint(models.Model):
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)
    lat = models.FloatField()
    lon = models.FloatField()
    state = models.CharField(
        max_length=16,
        choices=(
            ('', _('Unselected')),
            ('entered', _('Entered an Area')),
            ('exited', _('Exited an Area')),
            ('Do Button', _('Test Entry')),
            ('Do Note', _('Manual Entry')),
        )
    )
    description = models.TextField(blank=True)

import time
import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.urlresolvers import reverse
from django.db import IntegrityError, models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Stat(models.Model):
    created = models.DateTimeField(default=timezone.now)
    key = models.CharField(max_length=64)
    value = models.FloatField()

    class Meta:
        unique_together = (("created", "key"),)

    def insert(created, key, value):
        try:
            return Stat.objects.create(
                created=created,
                key=key,
                value=value
            )
        except IntegrityError:
            stat = Stat.objects.get(created=created, key=key)
            stat.value = value
            stat.save()
            return stat

    @property
    def created_unix(self):
        '''Unix timestamp in seconds'''
        return time.mktime(self.created.timetuple())


class Annotation(models.Model):
    created = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=64)
    tags = models.CharField(max_length=64)
    text = models.TextField()

    @property
    def created_unix(self):
        '''Unix timestamp in seconds'''
        return time.mktime(self.created.timetuple())


class StatMeta(models.Model):
    '''Meta information for rendering stats'''
    chart = models.CharField(max_length=64)
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=64)


class Countdown(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=128, blank=True)
    created = models.DateTimeField()
    label = models.CharField(max_length=36)
    calendar = models.URLField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='coutdown', verbose_name=_('owner'))
    meta = JSONField()
    public = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='simplestats/countdown', blank=True)

    def remaining(self):
        return self.created - timezone.localtime(timezone.now())

    def get_absolute_url(self):
        return reverse('api:countdown-detail', args=[self.pk])


class Chart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField()
    label = models.CharField(max_length=36)
    keys = models.CharField(max_length=36)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chart', verbose_name=_('owner'))
    meta = JSONField()
    public = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='simplestats/countdown', blank=True)

    def get_meta(self, key, default=None):
        try:
            return self.meta[key]
        except KeyError:
            return default
        except TypeError:
            return default


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    #owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='report', verbose_name=_('owner'))
    name = models.CharField(max_length=36)
    text = models.TextField(blank=True)
    html = models.TextField(blank=True)

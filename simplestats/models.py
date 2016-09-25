import time
import uuid

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import IntegrityError, models
from django.db.models.signals import post_save
from django.dispatch import receiver
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

    @classmethod
    def unique_keys(cls):
        for key in cls.objects.values_list('key', flat=True).distinct('key').order_by('key'):
            yield key

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

    public = models.BooleanField(default=False)
    allday = models.BooleanField(default=False)
    repeating = models.BooleanField(default=False)

    icon = models.ImageField(upload_to='simplestats/countdown', blank=True)
    more = models.URLField(blank=True)

    def remaining(self):
        return self.created - timezone.localtime(timezone.now())

    def get_absolute_url(self):
        return reverse('api:countdown-detail', args=[self.pk])


class Chart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField()
    label = models.CharField(max_length=64)
    keys = models.CharField(
        max_length=36,
        #choices=[(x, x) for x in Stat.unique_keys()]  # disable for now to assist in bootstrap
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chart', verbose_name=_('owner'))
    public = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='simplestats/countdown', blank=True)
    value = models.FloatField()
    more = models.URLField(blank=True)

    def refresh(self, value=None):
        if value:
            self.value = value
        else:
            latest = Stat.objects.filter(key=self.keys).latest('created')
            self.value = latest.value
        self.save()

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    #owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='report', verbose_name=_('owner'))
    name = models.CharField(max_length=36)
    text = models.TextField(blank=True)
    html = models.TextField(blank=True)


class Token(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    value = models.TextField()


@receiver(post_save, sender=Stat)
def update_chart_latest(sender, instance, *args, **kwargs):
    latest = Stat.objects.filter(key=instance.key).latest('created')
    for chart in Chart.objects.filter(keys=instance.key):
        chart.refresh(latest.value)

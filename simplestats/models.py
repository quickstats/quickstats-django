import os
import time
import uuid

from django.conf import settings
from django.db import IntegrityError, models
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


def _upload_to_path(instance, filename):
    root, ext = os.path.splitext(filename)
    return 'simplestats/{}/{}{}'.format(
        instance.__class__.__name__, instance.pk, ext).lower()


class Stat(models.Model):
    created = models.DateTimeField(default=timezone.now)
    key = models.CharField(max_length=128)
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


class Countdown(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=512, blank=True)
    created = models.DateTimeField()
    label = models.CharField(max_length=64)
    calendar = models.URLField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='coutdown', verbose_name=_('owner'))

    public = models.BooleanField(default=False)
    allday = models.BooleanField(default=False)
    repeating = models.BooleanField(default=False)

    icon = models.ImageField(upload_to=_upload_to_path, blank=True)
    more = models.URLField(blank=True)

    def remaining(self):
        return self.created - timezone.localtime(timezone.now())

    def get_absolute_url(self):
        return reverse('api:countdown-detail', args=[self.pk])


class Chart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now)
    label = models.CharField(max_length=64)
    unit = models.CharField(max_length=64, blank=True)
    keys = models.CharField(
        max_length=128,
        #choices=[(x, x) for x in Stat.unique_keys()]  # disable for now to assist in bootstrap
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chart', verbose_name=_('owner'))
    public = models.BooleanField(default=False)
    icon = models.ImageField(upload_to=_upload_to_path, blank=True)
    value = models.FloatField(default=0)
    more = models.URLField(blank=True)

    def record(self, timestamp, value):
        return Data.objects.create(
            timestamp=timestamp,
            parent=self,
            value=value
        )

    def upsert(self, timestamp, value):
        return Data.objects.update_or_create(
            timestamp=timestamp,
            parent=self,
            defaults={'value': value}
        )


class Data(models.Model):
    parent = models.ForeignKey(Chart, related_name='data_set')
    timestamp = models.DateTimeField()
    value = models.FloatField()


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='report', verbose_name=_('owner'))
    name = models.CharField(max_length=36)
    text = models.TextField(blank=True)

    class Meta:
        unique_together = ('date', 'owner', 'name')
        ordering = ['-date']

    def get_absolute_url(self):
        return reverse('stats:report-detail', args=[str(self.id)], current_app='stats')


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='location', verbose_name=_('owner'))
    name = models.CharField(max_length=36)

    class Meta:
        unique_together = ('owner', 'name',)

    def __str__(self):
        return '<Location: {}>'.format(self.name)

    def get_absolute_url(self):
        return reverse('stats:location-detail', args=[str(self.id)], current_app='stats')

    def record(self, **kwargs):
        return Movement.objects.create(location=self, **kwargs)


class Movement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=now)
    location = models.ForeignKey(Location)
    map = models.URLField()
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
    note = models.TextField(blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} {} {} {}'.format(self.location, self.state, self.map, self.created)

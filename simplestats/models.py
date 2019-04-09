from django.conf import settings
from django.db import models
from django.utils import timezone


class Widget(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField()
    public = models.BooleanField(default=False)
    series = models.ManyToManyField("simplestats.Series")


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget = models.ForeignKey("simplestats.Widget", on_delete=models.CASCADE)
    timestamp = models.DateField(default=timezone.now)


class Subscription(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget = models.ForeignKey("simplestats.Widget", on_delete=models.CASCADE)


class Series(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    public = models.BooleanField(default=False)


class Sample(models.Model):
    series = models.ForeignKey("simplestats.Series", on_delete=models.CASCADE)
    timestamp = models.DateField(default=timezone.now)
    value = models.FloatField()

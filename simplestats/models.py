from django.conf import settings
from django.db import models
from django.utils import timezone


class Widget(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField()
    public = models.BooleanField()
    publications = models.ManyToManyField(Series)


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE)


class Subscription(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE)


class Series(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    public = models.BooleanField()


class Sample(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    timestamp = models.DateField(default=timezone.now)
    value = models.FloatField()

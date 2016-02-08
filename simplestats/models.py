from django.db import models


class Stat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    key = models.TextField()
    value = models.FloatField()


class Countdown(models.Model):
    created = models.DateTimeField()
    label = models.CharField(max_length=36)
    calendar = models.URLField(null=True)

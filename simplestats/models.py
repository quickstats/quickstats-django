from django.db import models
from django.utils import timezone


class Stat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    key = models.TextField()
    value = models.FloatField()


class Countdown(models.Model):
    created = models.DateTimeField()
    label = models.CharField(max_length=36)
    calendar = models.URLField(blank=True)

    def remaining(self):
        return self.created - timezone.localtime(timezone.now())

from django.db import models


class Stat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    key = models.TextField()
    value = models.FloatField()


class Location(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    label = models.TextField()
    location = models.TextField()
    state = models.TextField()

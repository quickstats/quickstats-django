import logging

from celery import shared_task

import simplestats.models

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@shared_task()
def update_chart(pk):
    chart = simplestats.models.Chart.objects.get(pk=pk)
    latest = simplestats.models.Data.objects.filter(parent_id=pk).latest('timestamp')
    chart.value = latest.value
    chart.save()


@receiver(post_save, sender=simplestats.models.Stat)
def update_chart_latest(sender, instance, *args, **kwargs):
    latest = simplestats.models.Stat.objects.filter(key=instance.key).latest('created')
    for chart in simplestats.models.Chart.objects.filter(keys=instance.key):
        chart.value = latest.value
        chart.save()

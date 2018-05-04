import logging

from celery import shared_task

import simplestats.models

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@shared_task()
def update_chart(pk):
    chart = simplestats.models.Widget.objects.get(pk=pk)
    latest = simplestats.models.Sample.objects.filter(widget_id=pk).latest('timestamp')
    chart.value = latest.value
    chart.timestamp = latest.timestamp
    chart.save()


@receiver(post_save, sender='simplestats.Sample', dispatch_uid='simplestats-refresh-chart')
def hook_update_data(sender, instance, *args, **kwargs):
    update_chart.delay(instance.widget_id)

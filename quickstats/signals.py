import logging

from . import tasks

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender="quickstats.Sample", dispatch_uid="quickstats-refresh-chart")
def hook_update_chart(sender, instance, *args, **kwargs):
    tasks.update_chart.delay(instance.widget_id)


@receiver(post_save, sender="quickstats.Waypoint", dispatch_uid="quickstats-refresh-location")
def hook_update_location(sender, instance, *args, **kwargs):
    tasks.update_location.delay(instance.widget_id)

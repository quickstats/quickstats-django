import logging
import os

from pomodoro.models import Pomodoro

from simplestats.numerous import Numerous

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)

if 'NUMEROUS_KEY' in os.environ:
    logger.info('Registering numerous signals')

    @receiver(post_save, sender=Pomodoro)
    def my_callback(sender, instance, created, **kwargs):
        chart = 7919502141875764983

        # Only trigger updates for brand new objects
        if not created:
            return

        Numerous.update_value(chart, int(instance.created.timestamp()))
        Numerous.update_chart(chart, {
            'kind': 'timer',
            'label': instance.title,
            'visibility': 'private',
        })

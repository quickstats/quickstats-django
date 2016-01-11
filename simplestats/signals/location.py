import logging
import os

from position.models import Location

from simplestats.numerous import Numerous

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)

if 'NUMEROUS_KEY' in os.environ:
    logger.info('Registering numerous signals')

    @receiver(post_save, sender=Location)
    def my_callback(sender, instance, created, **kwargs):
        # Only trigger updates for brand new objects
        if not created:
            return

        if instance.state in ['entered', 'exited']:
            chart = 2178725227255461101
        else:
            chart = 6983546688771159792

        # Update timestamp
        Numerous.update_value(chart, int(instance.created.timestamp()))

        if instance.state == 'entered':
            Numerous.update_chart(chart, {
                'description': '場所に入った',
                'kind': 'timer',
                'label': instance.label,
                'moreURL': instance.location,
                'photoTreatment': {'gradientType': 'vertical', 'gradientColor1': '00bbaa', 'gradientColor2': '00dd00'},
                'visibility': 'private',
            })
        elif instance.state == 'exited':
            Numerous.update_chart(chart, {
                'description': '場所を出た',
                'kind': 'timer',
                'label': instance.label,
                'moreURL': instance.location,
                'photoTreatment': {'gradientType': 'vertical', 'gradientColor1': 'ff5588', 'gradientColor2': 'ff4466'},
                'visibility': 'private',
            })
        else:
            Numerous.update_chart(chart, {
                'description': '他のトリガー',
                'kind': 'timer',
                'label': instance.label,
                'moreURL': instance.location,
                'photoTreatment': {'gradientType': 'horizontal', 'gradientColor1': 'oa1cff', 'gradientColor2': '8076ff'},
                'visibility': 'private',
            })

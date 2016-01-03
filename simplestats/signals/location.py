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
    def my_callback(sender, instance, **kwargs):
        if instance.state in ['entered', 'exited']:
            chart = 2178725227255461101
        else:
            chart = 6983546688771159792

        # Update timestamp
        Numerous.update_value(chart, int(instance.created.timestamp()))

        if instance.state == 'entered':
            Numerous.update_chart(chart, {
                'label': '{}に入る'.format(instance.label),
                'kind': 'timer',
            })
        elif instance.state == 'exited':
            Numerous.update_chart(chart, {
                'label': '{}を出る '.format(instance.label),
                'kind': 'timer',
            })
        else:
            Numerous.update_chart(chart, {
                'label': '他の{}'.format(instance.label),
                'kind': 'timer',
            })

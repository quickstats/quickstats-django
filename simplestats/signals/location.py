import logging
import os

import requests
from position.models import Location

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)

if 'NUMEROUS_KEY' in os.environ:
    logger.info('Registering numerous signals')

    @receiver(post_save, sender=Location)
    def my_callback(sender, instance, **kwargs):
        requests.post('https://api.numerousapp.com/v2/metrics/2178725227255461101/events',
            auth=(os.environ.get('NUMEROUS_KEY'), ''),
            json={'value': int(instance.created.timestamp())})
        if instance.state == 'entered':
            requests.put('https://api.numerousapp.com/v2/metrics/2178725227255461101',
                auth=(os.environ.get('NUMEROUS_KEY'), ''),
                json={
                    'label': _('Entered an Area') + '' + instance.label,
                     'kind': 'timer'})
        if instance.state == 'exited':
            requests.put('https://api.numerousapp.com/v2/metrics/2178725227255461101',
                auth=(os.environ.get('NUMEROUS_KEY'), ''),
                json={
                    'label': _('Exited an Area') + '' + instance.label,
                     'kind': 'timer'})

        if instance.state == 'Do Note':
            requests.put('https://api.numerousapp.com/v2/metrics/2178725227255461101',
                auth=(os.environ.get('NUMEROUS_KEY'), ''),
                json={
                    'label': _('Manual Entry') + '' + instance.label,
                     'kind': 'timer'})

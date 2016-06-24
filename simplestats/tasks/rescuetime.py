'''
RescueTime Reports

Reports for https://www.rescuetime.com/

Manage keys: https://www.rescuetime.com/anapi/manage
API Docs: https://www.rescuetime.com/anapi/setup/documentation
'''
import datetime
import logging
import os

from celery.schedules import crontab
from celery.task.base import periodic_task

import simplestats.requests as requests
from simplestats.models import Stat

from django.utils import timezone

logger = logging.getLogger(__name__)

RESCUE_TIME_KEY = os.environ.get('RESCUE_TIME_KEY')

PRODUCTIVITY = {
    -2: 'rescuetime.verydistracting',
    -1: 'rescuetime.distracting',
    0: 'rescuetime.neutral',
    1: 'rescuetime.productive',
    2: 'rescuetime.veryproductive',
}

CATEGORY = {
    'Uncategorized': 'rescuetime.uncategorized'
}


@periodic_task(run_every=crontab(minute=0, hour=1))
def productivity():
    '''Collect daily stats from RescueTime'''
    now = timezone.localtime(timezone.now())

    response = requests.get('https://www.rescuetime.com/anapi/data', params={
        'key': RESCUE_TIME_KEY,
        'format': 'json',
        'resolution_time': 'day',
        'restrict_begin': now.today() - datetime.timedelta(days=7),
        'restrict_end': now.today(),
        'perspective': 'interval',
        'restrict_kind': 'productivity',
    })

    response.raise_for_status()
    data = response.json()

    for date, time, _, productivity in data['rows']:
        date = datetime.datetime.strptime(date, '%Y-%m-%dT00:00:00')
        Stat.insert(
            created=timezone.make_aware(date),
            key=PRODUCTIVITY[productivity],
            value=time,
        )


@periodic_task(run_every=crontab(minute=0, hour=1))
def category():
    '''Collect daily stats from RescueTime'''
    now = timezone.localtime(timezone.now())

    response = requests.get('https://www.rescuetime.com/anapi/data', params={
        'key': RESCUE_TIME_KEY,
        'format': 'json',
        'resolution_time': 'day',
        'restrict_begin': now.date() - datetime.timedelta(days=7),
        'restrict_end': now.date(),
        'perspective': 'interval',
        'restrict_kind': 'category',
    })

    response.raise_for_status()
    data = response.json()

    for date, time, _, category in data['rows']:
        if category not in CATEGORY:
            continue

        date = datetime.datetime.strptime(date, '%Y-%m-%dT00:00:00')
        Stat.insert(
            created=timezone.make_aware(date),
            key=CATEGORY[category],
            value=time,
        )

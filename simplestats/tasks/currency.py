'''
Get currency data for JPY from forecast.io

https://docs.openexchangerates.org/docs/latest-json
'''

import datetime
import logging
import os

from celery.schedules import crontab
from celery.task.base import periodic_task

import simplestats.requests as requests
from simplestats.models import Stat

logger = logging.getLogger(__name__)


@periodic_task(run_every=crontab(minute=0))
def collect():
        now = datetime.datetime.utcnow().replace(microsecond=0, second=0)
        url = 'https://openexchangerates.org/api/latest.json'
        result = requests.get(url, params={
            'app_id': os.environ.get('OPEN_EXCHANGE_RATES')
        })
        result.raise_for_status()
        json = result.json()
        Stat.objects.create(
            created=now,
            key='currency.USD.JPY',
            value=json['rates']['JPY']
        )

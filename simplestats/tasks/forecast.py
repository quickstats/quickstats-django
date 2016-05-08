'''
Get weather data for Fukuoka from forecast.io

https://developer.forecast.io/docs/v2
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
def fukuoka():
    now = datetime.datetime.utcnow().replace(microsecond=0, second=0)
    url = 'https://api.forecast.io/forecast/{0}/{1},{2}?units=si'.format(
        os.environ.get('FORECAST_IO'),
        33.5818585,
        130.3462494
    )
    result = requests.get(url)
    result.raise_for_status()
    json = result.json()

    Stat.objects.create(
        created=now,
        key='weather.fukuoka.temperature',
        value=json['currently']['temperature']
    )

    Stat.objects.create(
        created=now,
        key='weather.fukuoka.humidity',
        value=json['currently']['humidity']
    )

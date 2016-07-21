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

LOCATIONS = [
    (33.5818585, 130.3462494, 'weather.fukuoka.temperature', 'weather.fukuoka.humidity'),
    (35.766667, -78.633333, 'weather.raleigh.temperature', 'weather.raleigh.humidity'),
    (37.766667, -122.433333, 'weather.sanfrancisco.temperature', 'weather.sanfrancisco.humidity'),
]


@periodic_task(run_every=crontab(minute=0))
def collect(*args):
    if not args:
        for _args in LOCATIONS:
            logger.info('Queuing %s', _args)
            collect.delay(*_args)
        return

    lat, lng, temperature, humidity = args

    logger.info('Collecting %s %s', temperature, humidity)

    now = datetime.datetime.utcnow().replace(microsecond=0, second=0)
    url = 'https://api.forecast.io/forecast/{0}/{1},{2}?units=si'.format(
        os.environ.get('FORECAST_IO'),
        lat,
        lng,
    )
    result = requests.get(url)
    result.raise_for_status()
    json = result.json()

    Stat.objects.create(
        created=now,
        key=temperature,
        value=json['currently']['temperature']
    )

    Stat.objects.create(
        created=now,
        key=humidity,
        value=json['currently']['humidity']
    )

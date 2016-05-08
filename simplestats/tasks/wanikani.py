'''
Wanikani Tasks

Collect various stats and generate reports based on data from
https://www.wanikani.com/
'''

import datetime
import logging
import os

from celery.schedules import crontab
from celery.task.base import periodic_task

import simplestats.requests as requests
from simplestats.models import Countdown, Report, Stat

from django.template.loader import render_to_string
from django.utils import timezone

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.wanikani')
API_KEY = ''
logger = logging.getLogger(__name__)

if os.path.exists(CONFIG_PATH):
    logger.debug('Loading config from %s', CONFIG_PATH)
    with open(CONFIG_PATH) as f:
        API_KEY = f.read().strip()


# WaniKani typically updates on the 15 minute bounderies so we
# delay our stats check a bit in case their queue is slow
@periodic_task(run_every=crontab(minute='5,20,35,50'))
def collect():
    now = datetime.datetime.utcnow()
    url = 'https://www.wanikani.com/api/user/{}/study-queue'.format(API_KEY)
    result = requests.get(url)
    result.raise_for_status()
    json = result.json()
    user = json['user_information']
    info = json['requested_information']

    if info['reviews_available'] == 0:
        countdown = Countdown.objects.filter(label='Next Review').first()
        countdown.created = timezone.make_aware(datetime.datetime.fromtimestamp(info['next_review_date']))
        countdown.save()

    Stat.objects.create(
        created=now,
        key='wanikani.reviews',
        value=info['reviews_available']
    )
    Stat.objects.create(
        created=now,
        key='wanikani.lessons',
        value=info['lessons_available']
    )
    Stat.objects.create(
        created=now,
        key='wanikani.level',
        value=user['level']
    )


@periodic_task(run_every=crontab(minute=0, hour=0))
def report():
    '''Generate weekly report'''
    report = Report()
    report.date = timezone.now().date()

    url = 'https://www.wanikani.com/api/user/{}/study-queue'.format(API_KEY)
    result = requests.get(url)
    result.raise_for_status()
    json = result.json()
    report.name = __name__
    report.text = render_to_string('simplestats/reports/wanikani.txt', json)
    report.save()

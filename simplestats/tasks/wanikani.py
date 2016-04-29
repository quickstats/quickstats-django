import datetime
import logging
import os

from celery.schedules import crontab
from celery.task.base import periodic_task

import simplestats.requests as requests
from simplestats.models import Countdown, Stat
from simplestats.numerous import Numerous

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
        URL = 'https://www.wanikani.com/api/user/{}/study-queue'.format(API_KEY)
        result = requests.get(URL)
        json = result.json()
        user = json['user_information']
        info = json['requested_information']

        Numerous.update_value(1518834333051481998, user['level'])
        Numerous.update_value(7591292017638108494, info['lessons_available'])
        Numerous.update_value(5850886773862194952, info['reviews_available'])
        if info['reviews_available'] == 0:
            Numerous.update_value(8834312823618892099, info['next_review_date'])

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

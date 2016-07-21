'''
Use the Feedly API to graph count of unread items

https://developer.feedly.com/v3/developer/
https://developer.feedly.com/v3/streams/
'''
import datetime
from urllib import parse

from celery import shared_task
from celery.schedules import crontab
from celery.task.base import periodic_task

import simplestats.requests as requests
from simplestats.models import Stat, Token

FEEDS = [
    ('global.saved', 'feedly.count.saved'),
    ('Programming', 'feedly.count.programming'),
    ('勉強', 'feedly.count.studying'),
    ('生活', 'feedly.count.life'),
]


@periodic_task(run_every=crontab(minute=0, hour=0))
def scheduled():
    for args in FEEDS:
        unreadcount.delay(*args)


@shared_task
def unreadcount(feedly_tag, stats_key):
    '''
    Collect the unread count for a single feedly tag to store
    '''
    now = datetime.datetime.utcnow().replace(microsecond=0, second=0)
    user = Token.objects.get(id='feedly_id')
    token = Token.objects.get(id='feedly')
    # Need to ensure the tag is URL encoded
    tag = parse.quote('user/{}/tag/{}'.format(user.value, feedly_tag), safe='')

    response = requests.get(
        'http://cloud.feedly.com/v3/streams/{}/contents?count=500'.format(tag),
        headers={
            'Authorization': 'OAuth ' + token.value,
        })
    response.raise_for_status()
    data = response.json()

    Stat.objects.create(
        created=now,
        key=stats_key,
        value=len(data['items'])
    )

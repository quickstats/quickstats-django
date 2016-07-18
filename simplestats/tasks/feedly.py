'''
Use the Feedly API to graph count of unread items

https://developer.feedly.com/v3/developer/
https://developer.feedly.com/v3/streams/
'''
import datetime
from urllib import parse

from celery.schedules import crontab
from celery.task.base import periodic_task

import simplestats.requests as requests
from simplestats.models import Stat, Token


@periodic_task(run_every=crontab(minute=0, hour=0))
def unreadcount():
    now = datetime.datetime.utcnow().replace(microsecond=0, second=0)
    user = Token.objects.get(id='feedly_id')
    token = Token.objects.get(id='feedly')
    # Need to ensure the tag is URL encoded
    tag = parse.quote('user/{}/tag/global.saved'.format(user.value), safe='')

    response = requests.get(
        'http://cloud.feedly.com/v3/streams/{}/contents?count=500'.format(tag),
        headers={
            'Authorization': 'OAuth ' + token.value,
        })
    response.raise_for_status()
    data = response.json()

    Stat.objects.create(
        created=now,
        key='feedly.count.saved',
        value=len(data['items'])
    )

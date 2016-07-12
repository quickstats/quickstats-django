import datetime
import logging
import simplestats.requests as requests
from django.conf import settings
from celery.schedules import crontab
from celery.task.base import periodic_task

from simplestats.models import Stat, Token


logger = logging.getLogger(__name__)


@periodic_task(run_every=crontab(minute=0, hour=0))
def unreadcount():
    now = datetime.datetime.utcnow().replace(microsecond=0, second=0)
    token = Token.objects.get(id='pocket')

    response = requests.get(
        'https://getpocket.com/v3/get',
        headers={
            'X-Accept': 'application/json',
        },
        json={
            'consumer_key': settings.POCKET_CONSUMER_KEY,
            'access_token': token.value,
            'tag': '_untagged_',
            'state': 'all',
            'detailType': 'simple'
        })
    response.raise_for_status()
    unread_list = response.json()
    Stat.objects.create(
        created=now,
        key='pocket.count._untagged_',
        value=len(unread_list['list'])
    )

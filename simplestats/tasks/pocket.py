import datetime
import json
import logging

from celery import shared_task
from celery.schedules import crontab
from celery.task.base import periodic_task

import simplestats.requests as requests
from simplestats.models import Stat, Token

from django.conf import settings

TAGS = [
    ('_untagged_', 'pocket.count._untagged_'),
    ('_github', 'pocket.count.github'),
    ('_apps', 'pocket.count.apps'),
    ('_hn', 'pocket.count.hn'),
]

logger = logging.getLogger(__name__)


@periodic_task(run_every=crontab(minute=0, hour=0))
def scheduled():
    for args in TAGS:
        unreadcount.delay(*args)


@periodic_task(run_every=crontab(minute=0, hour=0))
def sort():
    '''Sort unread items into more reasonable lists'''
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
    actions = []
    for key in unread_list['list']:
        item = unread_list['list'][key]
        if item['given_url'].startswith('https://github.com/'):
            actions.append({
                'action': 'tags_replace',
                'item_id': key,
                'tags': '_github',
            })
        if item['given_url'].startswith('https://news.ycombinator.com'):
            actions.append({
                'action': 'tags_replace',
                'item_id': key,
                'tags': '_hn',
            })
        if item['given_url'].startswith('https://itunes.apple.com'):
            actions.append({
                'action': 'tags_replace',
                'item_id': key,
                'tags': '_apps',
            })

    if actions:
        logging.info('Updating %d items', len(actions))
        response = requests.get(
            'https://getpocket.com/v3/send',
            headers={
                'X-Accept': 'application/json',
            },
            params={
                'consumer_key': settings.POCKET_CONSUMER_KEY,
                'access_token': token.value,
                'actions': json.dumps(actions)
            })
        response.raise_for_status()


@shared_task
def unreadcount(pocket_tag, stat_key):
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
            'tag': pocket_tag,
            'state': 'all',
            'detailType': 'simple'
        })
    response.raise_for_status()
    unread_list = response.json()
    Stat.objects.create(
        created=now,
        key=stat_key,
        value=len(unread_list['list'])
    )

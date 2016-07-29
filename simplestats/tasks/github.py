'''
Track a simple count of Github issues
'''
import datetime

from celery.schedules import crontab
from celery.task.base import periodic_task

import simplestats.requests as requests
from simplestats.models import Stat


@periodic_task(run_every=crontab(minute=0, hour=0))
def issue_count():
    now = datetime.datetime.utcnow().replace(microsecond=0, second=0)
    url = 'https://api.github.com/search/issues?q=user:kfdm+state:open&per_page=100'
    result = requests.get(url, params={
        'accept': 'application/vnd.github.drax-preview+json'
    })
    result.raise_for_status()

    json = result.json()
    Stat.objects.create(
        created=now,
        key='github.issues.total',
        value=len(json['items'])
    )

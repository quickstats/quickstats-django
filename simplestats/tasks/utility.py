
import datetime
import logging
import os

from celery.task.base import periodic_task

import simplestats.requests as requests

logger = logging.getLogger(__name__)


@periodic_task(run_every=datetime.timedelta(minutes=5))
def healthchecks():
    requests.get(os.environ.get('HCHK_IO').strip()).raise_for_status()

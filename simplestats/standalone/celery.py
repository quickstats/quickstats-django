from __future__ import absolute_import

import logging
import os

import celery
import raven
from raven.contrib.celery import register_logger_signal, register_signal

from django.conf import settings  # noqa

logger = logging.getLogger(__name__)


class Celery(celery.Celery):
    def on_configure(self):
        if 'SENTRY_DSN' in os.environ:
            client = raven.Client(os.environ.get('SENTRY_DSN'))
            register_logger_signal(client)
            register_signal(client)

app = Celery('simplestats')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

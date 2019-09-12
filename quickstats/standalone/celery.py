from __future__ import absolute_import

import celery

app = celery.Celery("quickstats")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


from celery import shared_task
from prometheus_client.parser import text_string_to_metric_families

import simplestats.requests as requests
from simplestats import shortcuts

from django.contrib.auth.models import User


@shared_task()
def scrape(url, owner, labels):
    owner = User.objects.get(username=owner)
    result = requests.get(url)
    result.raise_for_status()

    for family in text_string_to_metric_families(result.text):
        for sample in family.samples:
            shortcuts.quick_record(
                metric=sample[0],
                labels=dict(sample[1], **labels),
                value=sample[2],
                owner=owner,
            )

import logging

from celery import shared_task

from django.contrib.auth.models import User
from django.utils import timezone

from simplestats.models import Widget

logger = logging.getLogger(__name__)


@shared_task()
def event(topic, data):
    logger.debug('Processing %s', topic)
    logger.debug('Data %s', data)

    try:
        widget = Widget.objects.get(
            meta__key='owntracks.tst',
            meta__value=data['wtst']
        )
    except Widget.DoesNotExist:
        _, username, device, _ = topic.split('/')
        owner = User.objects.get(username=username)
        widget = Widget.objects.create(
            title=data['desc'],
            description='Created by ' + device,
            owner=owner,
            type='location',
        )
        logger.info('Created widget %s', widget)
        widget.meta_set.create(key='owntracks.tst', value=data['wtst'])
    else:
        logger.info('found widget %s', widget)
        widget.timestamp = timezone.now()
        widget.save()
        logger.info('Updated widget timestamp %s', widget)

    # Mapping for Owntracks state to IFTTT
    state = 'entered' if data['event'] == 'enter' else 'exited'

    # TODO: For now we won't try to read tst from Owntracks but in the future
    # may be better to read that
    waypoint = widget.waypoint_set.create(
        lat=data['lat'],
        lon=data['lon'],
        state=state,
    )
    logger.info('Added waypoint %s to %s', waypoint, widget)

import datetime
import logging
from datetime import timedelta

import icalendar
from celery.task.base import periodic_task

import simplestats.models
import simplestats.requests as requests

from django.utils import timezone

logger = logging.getLogger(__name__)


@periodic_task(run_every=timedelta(minutes=30))
def update_calendars():
    now = timezone.localtime(timezone.now())
    for countdown in simplestats.models.Countdown.objects.exclude(calendar__exact=''):
        next_event = None

        response = requests.get(countdown.calendar)
        calendar = icalendar.Calendar.from_ical(response.text)
        if 'X-WR-CALNAME' in calendar:
            logger.info('Reading calendar: %s', calendar['X-WR-CALNAME'])
        for component in calendar.subcomponents:
            # Filter out non events
            if 'DTSTART' not in component:
                logger.debug('No DTSTART: %s', component.get('SUMMARY', component))
                continue

            # Filter out all day events
            if not isinstance(component['DTSTART'].dt, datetime.datetime):
                logger.debug('Filter out all day event: %s', component['SUMMARY'])
                continue
            if component['DTSTART'].dt < now:
                logger.debug('Filter out past event: %s', component['SUMMARY'])
                continue

            if next_event is None:
                logger.debug('Setting next to: %s', component['SUMMARY'])
                next_event = component
                continue

            if component['DTSTART'].dt < next_event['DTSTART'].dt:
                logger.debug('Setting next to: %s', component['SUMMARY'])
                next_event = component

        if next_event:
            countdown.label = next_event['SUMMARY']
            countdown.created = next_event['DTSTART'].dt
            countdown.save()
            logger.info('Updating date for %s to %s', countdown.label, countdown.created)

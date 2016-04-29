import datetime
import logging

import icalendar
from celery.task.base import periodic_task

import simplestats.models
import simplestats.requests as requests

from django.utils import timezone

logger = logging.getLogger(__name__)


@periodic_task(run_every=datetime.timedelta(minutes=30))
def update_calendars():
    now = timezone.localtime(timezone.now())
    for countdown in simplestats.models.Countdown.objects.exclude(calendar__exact=''):
        next_event = None
        include_all_day = isinstance(countdown.meta, dict) and 'all_day' in countdown.meta

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
                if include_all_day:
                    logger.debug('Converting to midnight date: %s', component['SUMMARY'])
                    component['DTSTART'] = icalendar.vDatetime(timezone.make_aware(datetime.datetime.combine(component['DTSTART'].dt, datetime.time.min)))
                else:
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

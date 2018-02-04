import datetime
import logging

from celery import shared_task
from celery.task.base import periodic_task
from dateutil.rrule import rrulestr

import icalendar

import simplestats.models
import simplestats.requests as requests

from django.utils import timezone

logger = logging.getLogger(__name__)


@periodic_task(run_every=datetime.timedelta(minutes=30))
def scheduled():
    # Schedule all of our widgets that have a calendar subscription to update
    for meta in simplestats.models.Meta.objects.filter(key='calendar.subscription'):
        update_countdown.delay(meta.widget_id)


@shared_task()
def update_countdown(pk):
    countdown = simplestats.models.Widget.objects.get(meta__pk=pk)
    logger.debug(countdown)

    countdown.timestamp = datetime.datetime.min
    now = timezone.localtime(timezone.now())
    end = now + datetime.timedelta(days=30)
    next_event = None
    next_time = None

    response = requests.get(countdown['calendar.subscription'])
    calendar = icalendar.Calendar.from_ical(response.text)
    if 'X-WR-CALNAME' in calendar:
        logger.info('Reading calendar: %s', calendar['X-WR-CALNAME'])
        countdown.description = 'Next event in %s' % calendar['X-WR-CALNAME']

    for component in calendar.subcomponents:
        # Filter out non events
        if 'DTSTART' not in component:
            logger.debug('No DTSTART: %s', component.get('SUMMARY', component))
            continue

        # Filter out all day events
        if not isinstance(component['DTSTART'].dt, datetime.datetime):
            if countdown['calendar.allday']:
                logger.debug('Converting to midnight date: %s', component['SUMMARY'])
                component['DTSTART'] = icalendar.vDatetime(timezone.make_aware(datetime.datetime.combine(component['DTSTART'].dt, datetime.time.min)))
            else:
                logger.debug('Filter out all day event: %s', component['SUMMARY'])
                continue

        if component['DTSTART'].dt < now:
            if 'RRULE' not in component or countdown['calendar.repeating'] is None:
                logger.debug('Filter out past event: %s', component['SUMMARY'])
                continue
            else:
                logger.debug('Processing RRULE')
                # Pull out our exclude dates into an easy list
                exdate = []
                if 'EXDATE' in component:
                    try:
                        for entry in component['EXDATE']:
                            for item in entry.dts:
                                exdate.append(item.dt.date())
                    except TypeError:
                        for item in component['EXDATE'].dts:
                            exdate.append(item.dt.date())

                for entry in rrulestr(
                        component['RRULE'].to_ical().decode('utf-8'),
                        dtstart=component['DTSTART'].dt).between(now, end):

                    if entry.date() in exdate:
                        continue

                    if next_event is None:
                        logger.debug('Setting next to: %s', component['SUMMARY'])
                        next_event = component
                        next_time = entry
                        break
                    if entry < next_time:
                        next_event = component
                        next_time = entry
                        break
                continue

        if next_event is None:
            logger.debug('Setting next to: %s', component['SUMMARY'])
            next_event = component
            next_time = component['DTSTART'].dt
            continue

        if component['DTSTART'].dt < next_time:
            logger.debug('Setting next to: %s', component['SUMMARY'])
            next_event = component
            next_time = component['DTSTART'].dt

    if next_event:
        countdown.timestamp = next_time
        countdown.title = next_event['SUMMARY']
        countdown.more = next_event['URL'] if 'URL' in next_event else ''
        countdown.save()
        logger.info('Updating date for %s to %s', countdown.title, countdown.timestamp)

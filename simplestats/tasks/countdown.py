import datetime
import logging

import icalendar
from celery.task.base import periodic_task
from dateutil.rrule import rrulestr

import simplestats.models
import simplestats.requests as requests

from django.utils import timezone

logger = logging.getLogger(__name__)


@periodic_task(run_every=datetime.timedelta(minutes=30))
def update_calendars():
    now = timezone.localtime(timezone.now())
    end = now + datetime.timedelta(days=30)
    for countdown in simplestats.models.Countdown.objects.exclude(calendar__exact=''):
        next_event = None
        next_time = None

        response = requests.get(countdown.calendar)
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
                if countdown.allday:
                    logger.debug('Converting to midnight date: %s', component['SUMMARY'])
                    component['DTSTART'] = icalendar.vDatetime(timezone.make_aware(datetime.datetime.combine(component['DTSTART'].dt, datetime.time.min)))
                else:
                    logger.debug('Filter out all day event: %s', component['SUMMARY'])
                    continue

            if component['DTSTART'].dt < now:
                if 'RRULE' not in component:
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

                        # If we find a valid date, then rewrite the original component with our
                        # corrected RRULE date
                        component['DTSTART'] = icalendar.vDatetime(
                            timezone.make_aware(datetime.datetime.combine(entry, datetime.time.min)))
                        break

            if next_event is None:
                logger.debug('Setting next to: %s', component['SUMMARY'])
                next_event = component['SUMMARY']
                next_time = component['DTSTART'].dt
                continue

            if component['DTSTART'].dt < next_time:
                logger.debug('Setting next to: %s', component['SUMMARY'])
                next_event = component['SUMMARY']
                next_time = component['DTSTART'].dt

        if next_event:
            countdown.label = next_event
            countdown.created = next_time
            countdown.save()
            logger.info('Updating date for %s to %s', countdown.label, countdown.created)

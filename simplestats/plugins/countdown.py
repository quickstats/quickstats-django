import datetime
import logging

import icalendar

import simplestats.models
import simplestats.requests as requests

from django.utils import timezone

logger = logging.getLogger(__name__)

class Countdown(object):
    def collect(self):
        now = timezone.localtime(timezone.now())
        for countdown in simplestats.models.Countdown.objects.exclude(calendar__exact=''):
            next_event = None

            response = requests.get(countdown.calendar)
            calendar = icalendar.Calendar.from_ical(response.text)
            for component in calendar.subcomponents:
                # Filter out non events
                if 'DTSTART' not in component:
                    continue
                if 'DTEND' not in component:
                    continue

                # Filter out all day events
                if not isinstance(component['DTSTART'].dt, datetime.datetime):
                    continue
                if component['DTSTART'].dt < now:
                    continue

                if next_event is None:
                    next_event = component
                    continue

                if component['DTSTART'].dt < next_event['DTSTART'].dt:
                    next_event = component

            if next_event:
                countdown.label = next_event['SUMMARY']
                countdown.created = next_event['DTSTART'].dt
                countdown.save()
                logger.info('Updating date for %s to %s', countdown.label, countdown.created)

        # We don't actually return any stats from this model
        return
        yield

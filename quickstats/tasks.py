import logging

import requests
from celery import shared_task
from celery.decorators import periodic_task
from celery.schedules import crontab

from . import models

from django.db.models import Sum

logger = logging.getLogger(__name__)


@shared_task()
def update_chart(pk):
    widget = models.Widget.objects.get(pk=pk, type="chart")
    latest = models.Sample.objects.filter(widget_id=pk).latest("timestamp")
    widget.value = latest.value
    widget.timestamp = latest.timestamp
    widget.save(update_fields=["value", "timestamp"])


@shared_task
def update_streak(pk):
    widget = models.Widget.objects.get(pk=pk, type="streak")

    # Update our timestamps
    from timezone.models import Timezone  # TODO fix later

    widget.timestamp = Timezone.for_user(owner=widget.owner).now()
    midnight = widget.timestamp.replace(hour=0, minute=0, second=0, microsecond=0)

    # Update our sample
    samples = models.Sample.objects.filter(widget_id=pk, timestamp__gte=midnight)
    widget.value = samples.aggregate(Sum("value"))["value__sum"]
    widget.save(update_fields=["value", "timestamp"])


@shared_task
def update_location(pk):
    widget = models.Widget.objects.get(pk=pk, type="location")
    latest = models.Waypoint.objects.filter(widget_id=pk).latest("timestamp")
    widget.timestamp = latest.timestamp
    widget.save(update_fields=["timestamp"])


@shared_task()
def scrape(pk):
    try:
        models.Scrape.objects.get(pk=pk).scrape()
    except ImportError:
        logger.exception("Error loading driver")
    except requests.HTTPError:
        logger.exception("Error scraping target")
    except Exception:
        logger.exception("Unhandled Exception")
    finally:
        return


schedule = {
    "15m": crontab(minute="5,20,35,50"),
    "30m": crontab(minute="25,55"),
    "1h": crontab(minute=0),
    "2h": crontab(minute=0, hour="*/2"),
    "1d": crontab(minute=0, hour=0),
}

for period in schedule:
    name = __name__ + ".schedule_" + period

    @periodic_task(run_every=schedule[period], name=name)
    def scheduled_scrape():
        for config in models.Scrape.objects.filter(period=period):
            scrape.delay(config.pk)

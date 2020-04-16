import datetime
import logging

import requests
from celery import shared_task
from celery.task.base import periodic_task
from timezone.models import Timezone

from . import models

from django.contrib.auth.models import User
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
    config = models.Scrape.objects.get(pk=pk)
    for entry in models.Scrape.drivers():
        if config.driver == entry.name:
            try:
                driver = entry.load()()
                driver.scrape(config)
            except ImportError:
                logger.exception("Error loading driver")
            except requests.HTTPError:
                logger.exception("Error scraping target")
            except Exception:
                logger.exception("Unhandled Exception")
            finally:
                return
    else:
        logger.error("Unknown driver %s", config.driver)


@periodic_task(run_every=datetime.timedelta(minutes=30))
def schedule_scrape():
    for config in models.Scrape.objects.all():
        scrape.delay(config.pk)


@shared_task
def owntracks_mqtt_event(topic, data):
    # https://owntracks.org/booklet/tech/json/#_typetransition
    if data.get("_type") != "transition":
        logger.warning("Not trsnition event")
        return
    topic = topic.split("/")
    user = User.objects.get(username=topic[1])

    widget, created = models.Widget.objects.get_or_create(
        setting__name="owntracks.tst",
        setting__value=data["wtst"],
        owner=user,
        defaults={
            "title": "OT " + data["desc"],
            "type": "location",
            "description": "Owntracks Location",
        },
    )
    if created:
        widget.setting_set.create(name="owntracks.tst", value=data["wtst"])
        logger.info("Created widget %s", widget)

    models.Waypoint.objects.get_or_create(
        defaults={"state": data["event"], "lat": data["lat"], "lon": data["lon"]},
        timestamp=datetime.datetime.fromtimestamp(data["tst"], datetime.timezone.utc),
        widget_id=widget.id,
    )


@shared_task
def owntracks_mqtt_waypoints(topic, data):
    # https://owntracks.org/booklet/tech/json/#_typewaypoint
    topic = topic.split("/")
    user = User.objects.get(username=topic[1])
    for waypoint in data["waypoints"]:
        widget, created = models.Widget.objects.get_or_create(
            setting__name="owntracks.tst",
            setting__value=waypoint["tst"],
            owner=user,
            defaults={
                "title": waypoint["desc"],
                "type": "location",
                "description": "Owntracks Location",
            },
        )
        if created:
            widget.setting_set.create(name="owntracks.tst", value=waypoint["tst"])
            logger.info("Created widget %s", widget)


@shared_task
def owntracks_mqtt_location(topic, data):
    # https://owntracks.org/booklet/tech/json/#_typelocation
    if data.get("_type") != "location":
        logger.warning("Not location event")
        return
    topic = topic.split("/")
    user = User.objects.get(username=topic[1])
    device = topic[2]

    widget, created = models.Widget.objects.get_or_create(
        setting__name="owntracks.device",
        setting__value=device,
        owner=user,
        defaults={
            "title": "OT " + data["tid"],
            "type": "location",
            "description": "Owntracks Device",
        },
    )
    if created:
        widget.setting_set.create(name="owntracks.device", value=device)

    models.Waypoint.objects.get_or_create(
        defaults={"state": "waypoint", "lat": data["lat"], "lon": data["lon"]},
        timestamp=datetime.datetime.fromtimestamp(data["tst"], datetime.timezone.utc),
        widget_id=widget.id,
    )

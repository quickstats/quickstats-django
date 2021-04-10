import logging

from django.utils import timezone

from quickstats.models import Widget

logger = logging.getLogger(__name__)


def quick_record(owner, value, **kwargs):
    labels = kwargs.pop("labels", {})
    defaults = kwargs.setdefault("defaults", {})
    defaults.setdefault("type", "chart")
    defaults.setdefault("value", value)

    # If we get a metric, we both want to set it
    # as one of our labels, but also default it to
    # the title we use for our widget
    if "metric" in kwargs:
        metric = kwargs.pop("metric")
        labels.setdefault("__name__", metric)
        defaults.setdefault("title", metric)

    if "timestamp" in kwargs:
        timestamp = kwargs.pop("timestamp")
        defaults.setdefault("timestamp", timestamp)
    else:
        timestamp = defaults.setdefault("timestamp", timezone.now())

    widget, _ = Widget.objects.lookup_or_create(owner=owner, labels=labels, **kwargs)
    sample = widget.sample_set.create(timestamp=timestamp, value=value)
    logger.debug("Created sample %r" % sample)
    return sample

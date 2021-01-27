import logging

from django.utils import timezone

from quickstats.models import Widget

logger = logging.getLogger(__name__)


def quick_record(owner, value, **kwargs):
    labels = kwargs.pop("labels", {})
    defaults = kwargs.setdefault("defaults", {})

    if "metric" in kwargs:
        metric = kwargs.pop("metric")
        labels.setdefault("__name__", metric)
        defaults.setdefault("title", metric)
    if "timestamp" not in kwargs:
        kwargs["timestamp"] = timezone.now()
    kwargs["value"] = value

    widget, _ = Widget.objects.lookup_or_create(
        owner=owner, type="chart", labels=labels, **kwargs
    )
    sample = widget.sample_set.create(timestamp=widget.timestamp, value=widget.value)
    logger.debug("Created sample %r" % sample)

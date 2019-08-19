import logging

from celery import shared_task

from . import models


logger = logging.getLogger(__name__)


@shared_task()
def update_chart(pk):
    widget = models.Widget.objects.get(pk=pk)
    if widget.type not in ["chart"]:
        return
    latest = models.Sample.objects.filter(widget_id=pk).latest("timestamp")
    widget.value = latest.value
    widget.timestamp = latest.timestamp
    widget.save(update_fields=["value", "timestamp"])

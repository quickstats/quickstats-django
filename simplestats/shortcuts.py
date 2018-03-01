import logging
from django.utils import timezone
from simplestats import models
from django.db.models import Q


logger = logging.getLogger(__name__)


def quick_record(owner, value, **kwargs):
    '''
    Chart.quick_record(
        owner=owner,
        metric='currency_rate',
        labels={
            'source': 'usd',
            'destination': 'jpy'
        },
        timestamp=now,
        value=json['rates']['JPY']
    )
    '''
    kwargs.setdefault('labels', {})
    kwargs.setdefault('type', 'chart')
    if 'metric' in kwargs:
        kwargs['labels'].setdefault('metric', kwargs.pop('metric'))
    if 'timestamp' not in kwargs:
        kwargs['timestamp'] = timezone.now()
    kwargs['value'] = value

    # Build a query looking for widgets that have all labels. If we do not
    # already have a widget, build a new one
    labels = kwargs.pop('labels')
    qs = models.Widget.objects
    for k, v in labels.items():
        qs = qs.filter(Q(label__name=k, label__value=v))
    try:
        widget = qs.get()
    except models.Widget.DoesNotExist:
        widget = models.Widget.objects.create(
            owner=owner,
            title=labels['metric'],
        )
        for k, v in labels.items():
            widget.label_set.create(name=k, value=v)

    # TODO: Optimize to be more robust
    # Add our new sample to our widget. We do a filter to see if we already
    # have a sample for this timestamp that needs to be updated, otherwise
    # we create a new sample. Perhaps can use sample_set.update ?
    for sample in widget.sample_set.filter(timestamp=kwargs['timestamp']):
        sample.value = value
        sample.save()
        return sample
    else:
        return widget.sample_set.create(
            timestamp=kwargs['timestamp'],
            value=value
        )

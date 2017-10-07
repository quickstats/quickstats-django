import logging
from django.utils import timezone
from simplestats import models


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
    if 'metric' in kwargs:
        kwargs['labels']['__name__'] = kwargs.pop('metric')
    if 'timestamp' not in kwargs:
        kwargs['timestamp'] = timezone.now()
    kwargs['value'] = value

    # TODO Temporary label
    # This is used to bridge our old lables to the new one
    _labels = kwargs['labels'].copy()
    kwargs['label'] = _labels.pop('__name__')
    if _labels:
        kwargs['label'] += str(_labels)
    kwargs['keys'] = kwargs['labels']

    # Pop a required parameter
    labels = kwargs.pop('labels')
    # Need to rename the value for our Chart Object
    kwargs['created'] = kwargs.pop('timestamp')

    chart, created = models.Chart.objects.get_or_create(
        owner=owner,
        labels=labels,
        defaults=kwargs
    )
    if created:
        logger.info('Created chart')
    return chart.upsert(kwargs['created'], value)

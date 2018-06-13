import datetime
import json

from django import template
from django.template import defaultfilters
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.filter()
def render_widget(widget, request):
    return render_to_string('simplestats/widget/{}.embed.html'.format(widget.type), {
        'object': widget,
        'request': request,
    })


@register.filter()
def gmap(waypoint):
    return 'http://maps.google.com?q={},{}'.format(waypoint.lat, waypoint.lon)


@register.filter()
def timediff(ts):
    if ts > timezone.now():
        return defaultfilters.timeuntil_filter(ts)
    return defaultfilters.timesince_filter(ts)


@register.filter()
def dataTable(obj):
    time_delta = datetime.timedelta(days=7)
    labels = [_('Datetime'), obj.title]
    dataTable = []

    for stat in obj.sample_set.order_by('timestamp').filter(timestamp__gte=datetime.datetime.now() - time_delta):
        dataTable.append([stat.timestamp.strftime("%Y-%m-%d %H:%M"), stat.value])

    return json.dumps([[str(_label) for _label in labels]] + dataTable)

from django import template
from django.template import defaultfilters
from django.template.loader import render_to_string
from django.utils import timezone

register = template.Library()


@register.filter()
def render_widget(widget):
    return render_to_string('simplestats/widget/{}.html'.format(widget.type), {
        widget.type: widget,
    })
    if widget.type == 'countdown':
        return render_to_string('simplestats/widget/countdown.html', {
            'countdown': widget,
        })
    if widget.type == 'chart':
        return render_to_string('simplestats/widget/chart.html', {
            'chart': widget,
        })
    return '*UNKNOWN*'


@register.filter()
def gmap(waypoint):
    return 'http://maps.google.com?q={},{}'.format(waypoint.lat, waypoint.lon)


@register.filter()
def timediff(ts):
    if ts > timezone.now():
        return defaultfilters.timeuntil_filter(ts)
    return defaultfilters.timesince_filter(ts)

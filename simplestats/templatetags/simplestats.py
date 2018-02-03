from django import template
from django.template.loader import render_to_string

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

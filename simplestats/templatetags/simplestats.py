from simplestats import models

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def formatted(widget):
    if widget.type == models.Widget.TYPE_COUNTDOWN:
        return mark_safe(
            "<time class='countdown' datetime='{}'>{}</time>".format(
                widget.timestamp.isoformat(), widget.timestamp.ctime()
            )
        )
    return widget.value

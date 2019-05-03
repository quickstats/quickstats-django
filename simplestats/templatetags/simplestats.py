from simplestats import models

from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse

register = template.Library()


@register.filter
def formatted(widget):
    if widget.type == 'countdown':
        return mark_safe(
            "<time class='countdown' datetime='{}'>{}</time>".format(
                widget.timestamp.isoformat(), widget.timestamp.ctime()
            )
        )
    return widget.value


@register.filter
def embedcode(widget, request):
    return '<iframe width="200" height="200" src="%s"></iframe>' % request.build_absolute_uri(
        reverse("api:widget-embed", args=(widget.pk,))
    )

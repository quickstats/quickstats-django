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
    return '<iframe width="250" height="250" src="%s" sandbox="allow-top-navigation" scrolling="no" frameborder="0"></iframe>' % request.build_absolute_uri(
        reverse("api:widget-embed", args=(widget.pk,))
    )

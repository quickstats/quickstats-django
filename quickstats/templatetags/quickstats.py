from django import template
from django.core.paginator import EmptyPage
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def formatted(widget):
    if widget.type == "countdown":
        return mark_safe(
            "<time class='countdown' datetime='{}'>{}</time>".format(
                widget.timestamp.isoformat(), widget.timestamp.ctime()
            )
        )
    return widget.value


@register.inclusion_tag("quickstats/embed_code.html", takes_context=True)
def embed_code(context, widget):
    return {
        "src_url": context["request"].build_absolute_uri(
            reverse("api:widget-embed", args=(widget.pk,))
        ),
    }


# Taken from here
# https://romanvm.pythonanywhere.com/post/bootstrap4-based-pagination-django-listview-30/


@register.inclusion_tag("quickstats/paginator.html", takes_context=True)
def render_paginator(context, adjacent_pages=3):
    """
    Inclusion tag

    Renders paginator for multi-page lists.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    :param context: parent template context
    :param adjacent_pages: the number of pages adjacent to the current
    :return: context for rendering paginator html code
    """
    start_page = max(context["page_obj"].number - adjacent_pages, 1)
    if start_page <= 3:
        start_page = 1

    end_page = context["page_obj"].number + adjacent_pages + 1
    if end_page >= context["paginator"].num_pages - 1:
        end_page = context["paginator"].num_pages + 1

    page_numbers = [
        n
        for n in range(start_page, end_page)
        if n in range(1, context["paginator"].num_pages + 1)
    ]

    try:
        next_ = context["page_obj"].next_page_number()
    except EmptyPage:
        next_ = None

    try:
        previous = context["page_obj"].previous_page_number()
    except EmptyPage:
        previous = None

    return {
        "page_obj": context["page_obj"],
        "paginator": context["paginator"],
        "page": context["page_obj"].number,
        "pages": context["paginator"].num_pages,
        "page_numbers": page_numbers,
        "next": next_,
        "previous": previous,
        "has_next": context["page_obj"].has_next(),
        "has_previous": context["page_obj"].has_previous(),
        "show_first": 1 not in page_numbers,
        "show_last": context["paginator"].num_pages not in page_numbers,
        "request": context["request"],
    }

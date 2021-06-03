import requests

from django.conf import settings

from quickstats.version import __VERSION__

DEFAULT_USER_AGENT = f"django-quickstats/{__VERSION__}"

USER_AGENT = getattr(settings, "USER_AGENT", DEFAULT_USER_AGENT)


def get(url, **kwargs):
    headers = kwargs.setdefault("headers", {})
    headers.setdefault("user-agent", USER_AGENT)
    return requests.get(url, **kwargs)


def post(url, **kwargs):
    headers = kwargs.setdefault("headers", {})
    headers.setdefault("user-agent", USER_AGENT)
    return requests.post(url, **kwargs)

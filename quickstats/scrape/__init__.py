import requests

from django import forms
from django.conf import settings

from quickstats.models import Scrape
from quickstats.version import __VERSION__


class FormScrape(forms.Form):
    url = forms.URLField()


DEFAULT_USER_AGENT = f"django-quickstats/{__VERSION__}"


class BaseScrape:
    form = FormScrape()

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.setdefault(
            "user-agent", getattr(settings, "USER_AGENT", DEFAULT_USER_AGENT)
        )

    def scrape(self, config: Scrape):
        raise NotImplementedError("Missing implementation")

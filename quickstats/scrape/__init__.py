import requests

from django import forms

from quickstats.client import USER_AGENT
from quickstats.models import Scrape


class FormScrape(forms.Form):
    url = forms.URLField()


class BaseScrape:
    form = FormScrape()

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.setdefault("user-agent", USER_AGENT)

    def scrape(self, config: Scrape):
        raise NotImplementedError("Missing implementation")

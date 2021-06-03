from django import forms

from quickstats.models import Scrape


class FormScrape(forms.Form):
    url = forms.URLField()


class BaseScrape:
    form = FormScrape()

    def scrape(self, config: Scrape):
        raise NotImplementedError("Missing implementation")

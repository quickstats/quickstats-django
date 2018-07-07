
import argparse

from simplestats.tasks.prometheus import scrape

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("url")
        parser.add_argument("owner")
        parser.add_argument("labels", nargs=argparse.REMAINDER)

    def handle(self, url, owner, labels, **kwargs):
        owner = User.objects.get(username=owner)

        labels = {y[0]: y[1] for y in [x.split("=") for x in labels]}

        scrape(url, owner, labels)

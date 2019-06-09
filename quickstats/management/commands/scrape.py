import sys

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from quickstats.prometheus import scrape_to_samples


class Command(BaseCommand):
    help = "Import metrics for testing"

    def add_arguments(self, parser):
        parser.add_argument("username")

    def handle(self, username, **options):
        user = User.objects.get(username=username)
        result = scrape_to_samples(sys.stdin.read(), user)

        print("\n".join(result))

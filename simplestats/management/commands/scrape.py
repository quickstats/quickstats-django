import sys

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse


class Command(BaseCommand):
    help = "Import metrics for testing"

    def add_arguments(self, parser):
        parser.add_argument('username')

    def handle(self, username, **options):
        client = Client()
        client.force_login(User.objects.get(username=username))
        result = client.post(
            reverse("prometheus:push", kwargs={"job": "test"}),
            data=sys.stdin.read(),
            content_type="text",
        )
        print(result)

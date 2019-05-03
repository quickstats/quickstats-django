import sys

from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse


class Command(BaseCommand):
    help = "Import metrics for testing"

    def add_arguments(self, parser):
        parser.add_argument("username")

    def handle(self, username, **options):
        token, _ = Token.objects.get_or_create(user=User.objects.get(username=username))
        client = Client()
        result = client.post(
            reverse("prometheus:push", kwargs={"token": token.pk}),
            data=sys.stdin.read(),
            content_type="text",
        )
        print(result)

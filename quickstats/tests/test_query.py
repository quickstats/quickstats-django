import time

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from quickstats import models, shortcuts


class SamplesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="SamplesTest")
        self.date = "2019-11-06T11:42:53.800762+00:00"

    def test_manager(self):
        print()
        self.assertEqual(models.Widget.objects.count(), 0)

        models.Widget.objects.lookup_or_create(
            labels={"A": 1, "B": 2, "__name__": "test"},
            owner=self.user,
            defaults={"timestamp": timezone.now(), "title": "test"},
        )

        time.sleep(1)
        models.Widget.objects.lookup_or_create(
            labels={"B": 2, "A": 1, "__name__": "test"},
            owner=self.user,
            defaults={"timestamp": timezone.now(), "title": "test"},
        )

        self.assertEqual(
            models.Widget.objects.count(), 1, "Should only be one new widget"
        )

    def test_shortcut(self):
        print()
        self.assertEqual(models.Widget.objects.count(), 0)
        shortcuts.quick_record(
            self.user,
            value=1,
            metric="test",
            labels={"A": 1, "B": 2},
            timestamp=timezone.now(),
        )
        time.sleep(1)
        shortcuts.quick_record(
            self.user,
            value=1,
            metric="test",
            labels={"B": 2, "A": 1},
            timestamp=timezone.now(),
        )
        self.assertEqual(
            models.Widget.objects.count(), 1, "Should only be one new widget"
        )

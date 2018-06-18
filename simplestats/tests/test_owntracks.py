import json
import os

from django.contrib.auth.models import User
from django.test import TestCase

from simplestats import models
from simplestats.tasks import owntracks

TEST_BASE = os.path.dirname(__file__)


class ShortcutTest(TestCase):
    def load_test(self, file):
        with open(os.path.join(TEST_BASE, file)) as fp:
            return json.loads(fp.read())

    def test_event_message(self):
        self.user = User.objects.create_user(username="foo")

        # Should create a single widget and waypoint
        owntracks.event(
            "owntracks/foo/test/event", self.load_test("owntracks.enter.json")
        )
        self.assertEqual(models.Widget.objects.count(), 1)
        self.assertEqual(models.Waypoint.objects.count(), 1)

        # Should create one more Waypoint
        owntracks.event(
            "owntracks/foo/test/event", self.load_test("owntracks.exit.json")
        )
        self.assertEqual(models.Widget.objects.count(), 1)
        self.assertEqual(models.Waypoint.objects.count(), 2)

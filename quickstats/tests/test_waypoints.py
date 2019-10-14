from quickstats import models, tasks

from django.contrib.auth.models import User
from django.test import TestCase, override_settings


class WaypointTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="WaypointTest")

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_owntracks_event(self):
        tasks.owntracks_mqtt_event(
            "owntracks/WaypointTest/device/waypoints",
            {
                "_type": "waypoints",
                "waypoints": [
                    {
                        "_type": "waypoint",
                        "tst": 1560375712,
                        "lat": 100.1,
                        "lon": 100.1,
                        "rad": 100,
                        "desc": "test-location",
                    }
                ],
            },
        )
        self.assertEqual(models.Waypoint.objects.count(), 1)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_owntracks_location(self):
        tasks.owntracks_mqtt_location(
            "owntracks/WaypointTest/device",
            {
                "batt": 100,
                "lon": 100.3543190608404,
                "acc": 65,
                "p": 102.1,
                "bs": 3,
                "vac": 10,
                "lat": 100.1,
                "inregions": ["test-location"],
                "t": "u",
                "conn": "w",
                "tst": 1571049037,
                "alt": 12,
                "_type": "location",
                "tid": "PR",
            },
        )
        self.assertEqual(models.Waypoint.objects.count(), 1)

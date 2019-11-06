from quickstats import models, tasks
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, override_settings


class WaypointTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="WaypointTest")

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_api(self):
        widget = models.Widget.objects.create(owner=self.user)
        # Create a single waypoint for testing
        widget.waypoint_set.create(lat=1, lon=1, state="waypoint")

        response = self.client.get(
            reverse("api-widget:waypoint-list", kwargs={"widget_pk": widget.pk})
        )
        self.assertEqual(response.status_code, 401, "anonymous user can not view")

        self.client.force_login(self.user)
        response = self.client.get(
            reverse("api-widget:waypoint-list", kwargs={"widget_pk": widget.pk})
        )
        self.assertEqual(response.status_code, 200, "can view after logging in")
        data = response.json()
        self.assertEqual(data["count"], 1, "Found one waypoint")

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_owntracks_waypoints(self):
        tasks.owntracks_mqtt_waypoints(
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
        self.assertEqual(models.Widget.objects.count(), 1)

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
        self.assertEqual(models.Widget.objects.count(), 1)
        self.assertEqual(models.Waypoint.objects.count(), 1)
        self.assertEqual(models.Setting.objects.count(), 1)

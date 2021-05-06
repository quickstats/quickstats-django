from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from quickstats import models


class WaypointTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="WaypointTest")
        self.date = "2019-11-06T11:42:53.800762+00:00"

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_api(self):
        widget = models.Widget.objects.create(owner=self.user)

        response = self.client.get(
            reverse("api-widget:waypoint-list", kwargs={"widget_pk": widget.pk})
        )
        self.assertEqual(response.status_code, 401, "anonymous user can not view")

        self.client.force_login(self.user)
        response = self.client.post(
            reverse("api-widget:waypoint-list", kwargs={"widget_pk": widget.pk}),
            data={"timestamp": self.date, "lat": 1, "lon": 1, "state": "waypoint"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201, "can post sample")

        response = self.client.get(
            reverse("api-widget:waypoint-list", kwargs={"widget_pk": widget.pk})
        )
        data = response.json()
        self.assertEqual(data["count"], 1, "Found one waypoint")

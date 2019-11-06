from quickstats import models

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse


class SamplesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="SamplesTest")
        self.date = "2019-11-06T11:42:53.800762+00:00"

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_api(self):
        widget = models.Widget.objects.create(owner=self.user)

        response = self.client.get(
            reverse("api-widget:sample-list", kwargs={"widget_pk": widget.pk})
        )
        self.assertEqual(response.status_code, 401, "anonymous user can not view")

        self.client.force_login(self.user)
        response = self.client.post(
            reverse("api-widget:sample-list", kwargs={"widget_pk": widget.pk}),
            data={"timestamp": self.date, "value": 1},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201, "can post sample")

        response = self.client.get(
            reverse("api-widget:sample-list", kwargs={"widget_pk": widget.pk})
        )
        data = response.json()
        self.assertEqual(data["count"], 1, "Found one sample")

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_visibility(self):
        viewer = User.objects.create(username="SampleViewer")

        widget = models.Widget.objects.create(owner=self.user)
        widget.sample_set.create(timestamp=self.date, value=1)

        self.client.force_login(viewer)
        response = self.client.get(
            reverse("api-widget:sample-list", kwargs={"widget_pk": widget.pk})
        )
        self.assertEqual(response.status_code, 403, "cannnot view private samples")

        widget.public = True
        widget.save(update_fields=["public"])

        response = self.client.get(
            reverse("api-widget:sample-list", kwargs={"widget_pk": widget.pk})
        )
        self.assertEqual(response.status_code, 200, "now can view public samples")
        data = response.json()
        self.assertEqual(data["count"], 1, "Found one sample")

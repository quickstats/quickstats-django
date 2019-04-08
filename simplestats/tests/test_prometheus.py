import os
from pathlib import Path

from django.test import TestCase
from django.urls import reverse
from simplestats import models
from django.contrib.auth import get_user_model

METRICS = Path(__file__).parent / "metrics.prom"


class PrometheusTest(TestCase):
    def test_push(self):
        user, _ = get_user_model().objects.get_or_create(username="promtest")
        self.client.force_login(user)

        with METRICS.open("r") as fp:
            response = self.client.post(
                reverse("push", args=("job_name",)),
                data=fp.read(),
                content_type="text/xml",
            )
        self.assertEqual(response.status_code, 200, "Succeeded Pushing metrics")
        self.assertEqual(models.Series.objects.count(), 2, "Found two series")
        self.assertEqual(models.Sample.objects.count(), 2, "Found two samples")

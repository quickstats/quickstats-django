from pathlib import Path

from simplestats import models

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

QUERY = Path(__file__).parent / "grafana.query.json"
SEARCH = Path(__file__).parent / "grafana.search.json"
ANNOTATION = Path(__file__).parent / "grafana.annotation.json"


class GrafanaTest(TestCase):
    def test_query(self):
        user, _ = get_user_model().objects.get_or_create(username="grafanatest")
        self.client.force_login(user)
        with QUERY.open("r") as fp:
            response = self.client.post(
                reverse("grafana:query"),
                data=fp.read(),
                content_type="application/json",
            )
        self.assertEqual(response.status_code, 200, "Successful grafana query")

    def test_search(self):
        user, _ = get_user_model().objects.get_or_create(username="grafanatest")
        one = models.Widget.objects.create(owner=user, title="foo1")
        two = models.Widget.objects.create(owner=user, title="foo2")
        models.Subscription.objects.create(owner=user, widget=one)
        models.Subscription.objects.create(owner=user, widget=two)

        self.client.force_login(user)
        with SEARCH.open("r") as fp:
            response = self.client.post(
                reverse("grafana:search"),
                data=fp.read(),
                content_type="application/json",
            )
        self.assertEqual(response.status_code, 200, "Successful grafana search")

    def test_annotations(self):
        user, _ = get_user_model().objects.get_or_create(username="grafanatest")
        self.client.force_login(user)
        with ANNOTATION.open("r") as fp:
            response = self.client.post(
                reverse("grafana:annotations"),
                data=fp.read(),
                content_type="application/json",
            )
        self.assertEqual(response.status_code, 200, "Successful grafana annotations")

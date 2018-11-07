
import os

from rest_framework.authtoken.models import Token

from simplestats.models import Sample

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

TEST_BASE = os.path.dirname(__file__)


class PrometheusTest(TestCase):
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_write(self):
        user = User.objects.create_user(username="foo")
        token = Token.objects.create(user=user)

        with open(os.path.join(TEST_BASE, 'test.prom')) as fp:
            response = self.client.post(
                reverse('pushgateway', kwargs={'api_key': token.key}),
                content_type='application/binary',
                data=fp.read(),
            )

        self.assertEqual(response.status_code, 202)
        self.assertEqual(Sample.objects.count(), 3)

from simplestats.models import Widget

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class GrafanaTest(TestCase):
    def setup(self):
        self.user = User.objects.create_user(id=999, username="Foo")
        self.client.force_login(self.user)

        Widget.objects.create(
            owner=self.user
        )

    def test_search(self):
        result = self.client.post(reverse('api:widget-search'), {
            'rules': 'foo'
        })
        print(result)

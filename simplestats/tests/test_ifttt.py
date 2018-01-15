import datetime
import json


from simplestats import models

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class IFTTTTest(TestCase):
    def test_entered(self):
        self.user = User.objects.create_user(username='foo')
        self.time = datetime.datetime(2017, 6, 8, 14, 18, tzinfo=datetime.timezone.utc)

        self.location = models.Widget.objects.create(
            title='Location Test',
            owner=self.user,
            type='location',
        )

        response = self.client.post(
            reverse('api:widget-ifttt', args=(self.location.slug,)),
            content_type='application/json',
            data=json.dumps({
                'state': 'entered',
                'label': 'Foo',
                'location': 'https://maps.google.com/?q=1,1',
                'timezone': 'Asia/Tokyo',
                'created': "June 08, 2017 at 11:18P",
            }),
        )

        self.assertEqual(response.status_code, 200)
        wp = models.Waypoint.objects.get()
        self.assertEqual(wp.state, 'entered')
        self.assertEqual(wp.timestamp, self.time)

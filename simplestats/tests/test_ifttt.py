import datetime
import json


from simplestats import models

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class IFTTTTest(TestCase):
    def test_entered(self):
        self.user = User.objects.create_user(username='foo')
        self.time = datetime.datetime(2017, 6, 8, 21, 30)

        self.location = models.Location.objects.create(name='Foo', owner=self.user)
        print(self.location)

        response = self.client.post(
            reverse('api:location-ifttt', args=(self.location.id,)),
            content_type='application/json',
            data=json.dumps({
                'state': 'entered',
                'label': 'Foo',
                'location': 'https://maps.google.com/?q=1,1',
                'created': str(self.time)
            }),
        )
        self.assertEqual(response.status_code, 200)
        self.movement = models.Movement.objects.get()
        self.assertEqual(self.movement.state, 'entered')
        print(self.movement)

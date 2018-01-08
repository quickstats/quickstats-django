import json
import datetime
from simplestats import models
from simplestats.shortcuts import quick_record

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone


class ShortcutTest(TestCase):
    def test_record(self):
        ts = timezone.now()
        owner = User.objects.create_user(username='foo')

        # Add a record
        result = quick_record(
            owner=owner,
            metric='currency_rate',
            labels={
                'source': 'usd',
                'destination': 'jpy'
            },
            timestamp=ts,
            value=12.34
        )

        # Test replacing the same timestamp
        result = quick_record(
            owner=owner,
            metric='currency_rate',
            labels={
                'source': 'usd',
                'destination': 'jpy'
            },
            timestamp=ts,
            value=9001
        )

        # Test with 'later' timestamp
        result = quick_record(
            owner=owner,
            metric='currency_rate',
            labels={
                'source': 'usd',
                'destination': 'jpy'
            },
            timestamp=ts + datetime.timedelta(seconds=1),
            value=12.34
        )

        self.assertEqual(models.Widget.objects.count(), 1)
        self.assertEqual(models.Sample.objects.count(), 2)
        self.assertEqual(models.Label.objects.count(), 3)

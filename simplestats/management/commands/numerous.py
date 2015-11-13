from django.core.management.base import BaseCommand
import requests
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get('https://api.numerousapp.com/v1/users/me/metrics', auth=(os.getenv('NUMEROUS_KEY'), ''))
        response.raise_for_status()
        for metric in response.json():
            print('Label:', metric['label'], metric['id'], metric['latestEventUpdated'])
            print('Description:', metric['description'])
            print('Link:', metric['links']['self'])
            print('Embed:', metric['links']['embed'])
            print()

import os
import pprint

import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help ='''Print out debugging information about current Numerous acccount'''

    def add_arguments(self, parser):
        parser.add_argument('--visibility', choices=['public', 'private'])

    def handle(self, *args, **options):
        response = requests.get('https://api.numerousapp.com/v1/users/me/metrics', auth=(os.getenv('NUMEROUS_KEY'), ''))
        response.raise_for_status()
        for metric in response.json():
            if options['visibility'] and options['visibility'] != metric['visibility']:
                continue
            self.stdout.write('Label: {0} {1} {2}'.format(metric['label'], metric['id'], metric['latestEventUpdated']))
            self.stdout.write('Privacy: {0}'.format('Private' if metric['private'] else 'Public'))
            self.stdout.write('Description: {0}'.format(metric['description']))
            self.stdout.write('Link: {0}'.format(metric['links']['self']))
            self.stdout.write('Embed: {0}'.format(metric['links']['embed']))
            if options['verbosity'] > 1:
                self.stdout.write(pprint.pformat(metric))
            self.stdout.write('*' * 80)

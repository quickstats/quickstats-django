from pkg_resources import working_set

from django.core.management.base import BaseCommand
from simplestats.models import Stat


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('group')

    def handle(self, *args, **options):
        for entry in working_set.iter_entry_points('simplestats.{0}'.format(options['group'])):
            module = entry.load()
            for timestamp, key, value in module().collect():
                stat = Stat()
                stat.created = timestamp
                stat.key = key
                stat.value = value
                stat.save()

from pkg_resources import working_set

from django.core.management.base import BaseCommand
from simplestats.models import Stat
from simplestats.constants import TIME_PERIODS


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('group', nargs='?', choices=TIME_PERIODS)

    def handle(self, *args, **options):
        if options['group'] == None:
            for time in TIME_PERIODS:
                self.stdout.write(time)
                for entry in working_set.iter_entry_points('simplestats.{0}'.format(time)):
                    self.stdout.write(str(entry))
            return

        for entry in working_set.iter_entry_points('simplestats.{0}'.format(options['group'])):
            module = entry.load()
            for timestamp, key, value in module().collect():
                stat = Stat()
                stat.created = timestamp
                stat.key = key
                stat.value = value
                stat.save()

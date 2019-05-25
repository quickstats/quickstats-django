
from simplestats.models import Widget

from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('src')
        parser.add_argument('dst')
        parser.add_argument('--force', action='store_true')

    def handle(self, src, dst, force, **kwargs):
        src = Widget.objects.get(pk=src)
        dst = Widget.objects.get(pk=dst)

        print('Source:', src)
        print('Destination:', dst)
        print('Merging', src.data_set.count(), 'into', dst.data_set.count())

        src.owner, _ = User.objects.get_or_create(username='merged-chart')

        if not dst.keys:
            print('Replacing', dst.keys, 'with', src.keys)
            dst.keys = src.keys
        if not dst.labels:
            print('Replacing', dst.labels, 'with', src.labels)
            dst.labels = src.labels
        if force:
            rst = src.data_set.update(parent=dst)
            print(rst)
            dst.save()
            src.save()

            print('http://{}{}'.format(get_current_site(None).domain, dst.get_absolute_url()))

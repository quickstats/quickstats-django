# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-08 10:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplestats', '0002_countdown'),
    ]

    operations = [
        migrations.RenameField(
            model_name='countdown',
            old_name='key',
            new_name='label',
        ),
    ]

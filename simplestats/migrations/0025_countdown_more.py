# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 01:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simplestats', '0024_auto_20160723_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='countdown',
            name='more',
            field=models.URLField(blank=True),
        ),
    ]
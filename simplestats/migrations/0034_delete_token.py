# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-02 13:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplestats', '0033_auto_20170102_0856'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Token',
        ),
    ]

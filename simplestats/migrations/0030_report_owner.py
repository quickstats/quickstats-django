# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 01:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simplestats', '0029_auto_20160925_0436'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='report', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
            preserve_default=False,
        ),
    ]

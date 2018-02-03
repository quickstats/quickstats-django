# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-08 09:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simplestats.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('simplestats', '0041_chart_labels'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('value', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=64)),
                ('value', models.TextField()),
                ('output', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Waypoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('state', models.CharField(choices=[('', 'Unselected'), ('entered', 'Entered an Area'), ('exited', 'Exited an Area'), ('Do Button', 'Test Entry'), ('Do Note', 'Manual Entry')], max_length=16)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True)),
                ('public', models.BooleanField(default=False)),
                ('icon', models.ImageField(blank=True, upload_to=simplestats.models._upload_to_path)),
                ('value', models.FloatField(default=0)),
                ('more', models.URLField(blank=True)),
                ('type', models.CharField(choices=[('chart', 'Chart'), ('countdown', 'Countdown'), ('location', 'Location')], max_length=32)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
        ),
        migrations.AddField(
            model_name='waypoint',
            name='widget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simplestats.Widget'),
        ),
        migrations.AddField(
            model_name='sample',
            name='widget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simplestats.Widget'),
        ),
        migrations.AddField(
            model_name='note',
            name='widget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simplestats.Widget'),
        ),
        migrations.AddField(
            model_name='meta',
            name='widget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simplestats.Widget'),
        ),
        migrations.AddField(
            model_name='label',
            name='widget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simplestats.Widget'),
        ),
        migrations.AlterUniqueTogether(
            name='sample',
            unique_together=set([('widget', 'timestamp')]),
        ),
        migrations.AlterUniqueTogether(
            name='meta',
            unique_together=set([('widget', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='label',
            unique_together=set([('widget', 'name')]),
        ),
    ]

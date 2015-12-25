# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=64, blank=True)),
                ('state', models.CharField(max_length=64, blank=True)),
                ('country', models.CharField(max_length=64, blank=True)),
                ('latitude', models.FloatField(max_length=64, null=True, blank=True)),
                ('longitude', models.FloatField(max_length=64, null=True, blank=True)),
                ('timestamp', models.DateTimeField()),
                ('status_description', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tracking_no', models.CharField(max_length=30)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='shipment',
            field=models.ForeignKey(to='goingpostal_app.Shipment'),
        ),
    ]

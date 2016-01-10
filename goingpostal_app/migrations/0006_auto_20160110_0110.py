# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goingpostal_app', '0005_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailaccount',
            name='access_token',
        ),
        migrations.RemoveField(
            model_name='emailaccount',
            name='refresh_token',
        ),
    ]

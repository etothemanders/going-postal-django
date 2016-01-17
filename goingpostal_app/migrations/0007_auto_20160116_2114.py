# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goingpostal_app', '0006_auto_20160110_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='status_description',
            field=models.CharField(max_length=128),
        ),
    ]

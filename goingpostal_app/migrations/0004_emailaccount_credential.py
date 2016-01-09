# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import oauth2client.django_orm


class Migration(migrations.Migration):

    dependencies = [
        ('goingpostal_app', '0003_flowmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailaccount',
            name='credential',
            field=oauth2client.django_orm.CredentialsField(null=True),
        ),
    ]

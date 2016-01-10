# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goingpostal_app', '0004_emailaccount_credential'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gmail_id', models.CharField(max_length=64)),
                ('email_account', models.ForeignKey(to='goingpostal_app.EmailAccount')),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-03 22:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0004_auto_20161203_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='last_seen',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 12, 3, 22, 59, 13, 907341, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
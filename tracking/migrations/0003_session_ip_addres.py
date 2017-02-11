# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-03 20:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_auto_20161130_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='ip_addres',
            field=models.GenericIPAddressField(default='0.0.0.0'),
            preserve_default=False,
        ),
    ]

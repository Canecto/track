# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-18 00:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0009_auto_20161204_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='cookie',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]

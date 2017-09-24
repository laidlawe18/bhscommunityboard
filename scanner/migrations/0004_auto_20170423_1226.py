# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-23 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0003_auto_20170422_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='checked_in',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checkout',
            name='date_returned',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]

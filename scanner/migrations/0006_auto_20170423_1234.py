# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-23 12:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0005_auto_20170423_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='date_returned',
            field=models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0)),
        ),
    ]

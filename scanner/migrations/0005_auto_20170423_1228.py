# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-23 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0004_auto_20170423_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='date_returned',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

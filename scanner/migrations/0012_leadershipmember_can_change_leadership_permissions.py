# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-03 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0011_auto_20170903_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadershipmember',
            name='can_change_leadership_permissions',
            field=models.BooleanField(default=False),
        ),
    ]

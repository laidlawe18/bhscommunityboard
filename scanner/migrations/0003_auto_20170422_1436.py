# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-22 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0002_checkoutitem_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkoutitem',
            name='default_checkout_time',
            field=models.IntegerField(),
        ),
    ]

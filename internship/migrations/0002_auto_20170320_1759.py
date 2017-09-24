# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-20 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internshipopportunity',
            name='name',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='internshipopportunity',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

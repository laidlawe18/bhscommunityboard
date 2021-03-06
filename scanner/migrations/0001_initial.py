# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-19 00:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_checked_out', models.DateTimeField()),
                ('date_due', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CheckoutItem',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('default_checkout_time', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='checkout',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scanner.CheckoutItem'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scanner.Person'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-13 01:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_auto_20171112_2346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='language',
        ),
        migrations.AddField(
            model_name='corpus',
            name='language',
            field=models.CharField(blank=True, default='en-us', max_length=10),
        ),
    ]

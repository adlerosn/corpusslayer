# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-19 04:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mxpost', '0002_auto_20171119_0446'),
    ]

    operations = [
        migrations.RenameField(
            model_name='corpusmxposted',
            old_name='tags',
            new_name='postags',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-16 02:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unitexgramlab', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='corpusprocessed',
            name='aec',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='corpusprocessed',
            name='fsttext',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='corpusprocessed',
            name='fsttexttagged',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='corpusprocessed',
            name='sentences',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='corpusprocessed',
            name='tagfreq',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='corpusprocessed',
            name='taggedfreq',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='corpusprocessed',
            name='wordfreq',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='corpusprocessed',
            name='wordlist',
            field=models.TextField(blank=True, null=True),
        ),
    ]

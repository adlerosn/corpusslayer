# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-17 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unitexgramlab', '0002_auto_20171116_0221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corpusprocessed',
            name='aec',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='corpusprocessed',
            name='fsttext',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='corpusprocessed',
            name='fsttexttagged',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='corpusprocessed',
            name='sentences',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='corpusprocessed',
            name='tagfreq',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='corpusprocessed',
            name='taggedfreq',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='corpusprocessed',
            name='wordfreq',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='corpusprocessed',
            name='wordlist',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]

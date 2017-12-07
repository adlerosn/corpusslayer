# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-25 04:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_auto_20171113_0114'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='corpus',
            options={'verbose_name': 'Corpus'},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'Document'},
        ),
        migrations.AddField(
            model_name='document',
            name='source',
            field=models.CharField(default='', max_length=255, verbose_name='source'),
        ),
        migrations.AlterField(
            model_name='corpus',
            name='comments',
            field=models.TextField(default='', verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='corpus',
            name='language',
            field=models.CharField(blank=True, default='en-us', max_length=10, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='corpus',
            name='title',
            field=models.CharField(default='', max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='document',
            name='text',
            field=models.TextField(blank=True, default='', verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(default='', max_length=255, verbose_name='title'),
        ),
    ]

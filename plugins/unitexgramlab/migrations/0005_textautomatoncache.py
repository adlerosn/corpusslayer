# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-18 19:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unitexgramlab', '0004_auto_20171117_2310'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextAutomatonCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('svg', models.BinaryField(blank=True, null=True)),
                ('pdf', models.BinaryField(blank=True, null=True)),
                ('jpg', models.BinaryField(blank=True, null=True)),
                ('corpus', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='text_automaton', to='unitexgramlab.CorpusProcessed')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

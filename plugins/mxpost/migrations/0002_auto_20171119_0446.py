# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-19 04:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0007_auto_20171113_0114'),
        ('mxpost', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorpusMxposted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('tags', models.TextField(blank=True, null=True)),
                ('corpus', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mxpost_tag_cache', to='application.Corpus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='corpusmxterminated',
            name='corpus',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mxpost_snt_cache', to='application.Corpus'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-12 23:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0004_corpus_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='tags_created', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
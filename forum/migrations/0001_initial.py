# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-28 21:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import forum.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='deleted',
            field=models.BooleanField(default=False)),
        ),
    ]

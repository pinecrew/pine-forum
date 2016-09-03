# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-03 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20160903_1322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='date',
            new_name='time',
        ),
        migrations.AddField(
            model_name='thread',
            name='title',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
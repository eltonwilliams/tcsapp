# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-19 14:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchdog', '0002_auto_20171219_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='call_comment',
        ),
        migrations.RemoveField(
            model_name='store',
            name='call_date',
        ),
        migrations.RemoveField(
            model_name='store',
            name='user',
        ),
    ]

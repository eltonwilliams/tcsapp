# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-09 10:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchdog', '0010_yealink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yealink',
            name='ip_address',
        ),
    ]

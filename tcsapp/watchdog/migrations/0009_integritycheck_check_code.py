# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-07 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchdog', '0008_integritycheck'),
    ]

    operations = [
        migrations.AddField(
            model_name='integritycheck',
            name='check_code',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
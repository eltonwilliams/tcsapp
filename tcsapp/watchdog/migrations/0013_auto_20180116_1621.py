# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-16 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchdog', '0012_auto_20180116_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextinvoice',
            name='code',
            field=models.CharField(default=b'##', max_length=2, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-18 07:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchdog', '0013_auto_20180116_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='integritycheck',
            name='code',
        ),
        migrations.AlterField(
            model_name='integritycheck',
            name='check_id',
            field=models.IntegerField(primary_key=True),
        ),
        migrations.AlterField(
            model_name='integritycheck',
            name='slave',
            field=models.CharField(default=b'###', max_length=3, primary_key=True, serialize=False),
        ),
    ]

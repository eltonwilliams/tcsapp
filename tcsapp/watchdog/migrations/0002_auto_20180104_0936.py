# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-04 07:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchdog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nextinvoice',
            name='id',
        ),
        migrations.AddField(
            model_name='nextinvoice',
            name='code',
            field=models.OneToOneField(default='DD', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='watchdog.Store'),
            preserve_default=False,
        ),
    ]

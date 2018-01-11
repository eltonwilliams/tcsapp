# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-04 09:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchdog', '0003_auto_20180104_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextinvoice',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watchdog.Store'),
        ),
        migrations.AlterField(
            model_name='nextinvoice',
            name='invoice',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
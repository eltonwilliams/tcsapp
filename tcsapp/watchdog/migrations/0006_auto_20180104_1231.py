# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-04 10:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchdog', '0005_auto_20180104_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextinvoice',
            name='code_id',
            field=models.ForeignKey(db_column=b'code', on_delete=django.db.models.deletion.CASCADE, to='watchdog.Store'),
        ),
    ]
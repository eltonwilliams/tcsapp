# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-19 12:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('code', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('area_manager', models.TextField()),
                ('area_manager_tel', models.TextField()),
                ('store_manager', models.TextField()),
                ('store_manager_tel', models.TextField()),
                ('trainee_manager', models.TextField()),
                ('trainee_manager_tel', models.TextField()),
                ('call_date', models.DateTimeField(blank=True, null=True)),
                ('call_comment', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
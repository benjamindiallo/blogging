# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20170407_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='biography',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]

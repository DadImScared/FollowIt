# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-08 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_unwatchedepisode'),
    ]

    operations = [
        migrations.AddField(
            model_name='unwatchedepisode',
            name='watched',
            field=models.BooleanField(default=False),
        ),
    ]
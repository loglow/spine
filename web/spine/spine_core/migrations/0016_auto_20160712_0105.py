# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 05:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spine_core', '0015_auto_20160712_0052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repo',
            name='projects',
        ),
        migrations.AddField(
            model_name='project',
            name='repos',
            field=models.ManyToManyField(to='spine_core.Repo'),
        ),
    ]

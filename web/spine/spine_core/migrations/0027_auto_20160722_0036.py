# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 04:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spine_core', '0026_auto_20160722_0019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='assigned_to',
            new_name='assigned',
        ),
        migrations.AlterField(
            model_name='file',
            name='depends',
            field=models.ManyToManyField(blank=True, to='spine_core.File'),
        ),
    ]
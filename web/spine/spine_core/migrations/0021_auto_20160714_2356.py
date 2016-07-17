# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 03:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spine_core', '0020_auto_20160712_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depend',
            name='depend_modified',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='depend',
            name='depend_version',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='depend',
            name='master_modified',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='depend',
            name='master_version',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='file',
            name='hash',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='file',
            name='modified',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='duration',
            field=models.DurationField(null=True),
        ),
    ]
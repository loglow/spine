# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 00:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spine_core', '0003_auto_20160709_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='repo',
            name='url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='depend',
            name='dependency_version',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='depend',
            name='master_version',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='last_version',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='repo',
            name='repo_type',
            field=models.CharField(choices=[('NONE', 'None'), ('SVN', 'Subversion'), ('MERC', 'Mercurial'), ('GIT', 'Git')], max_length=4),
        ),
        migrations.AlterField(
            model_name='repo',
            name='root_path',
            field=models.FilePathField(allow_files=False, allow_folders=True, path='/', recursive=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 21:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_version', models.PositiveIntegerField(default=0)),
                ('depend_version', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Repo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('root_path', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spine_core.Repo'),
        ),
        migrations.AddField(
            model_name='edge',
            name='depend_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depend_set', to='spine_core.File'),
        ),
        migrations.AddField(
            model_name='edge',
            name='main_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_set', to='spine_core.File'),
        ),
    ]

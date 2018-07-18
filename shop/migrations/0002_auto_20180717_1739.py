# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-17 16:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='free',
        ),
        migrations.AddField(
            model_name='book',
            name='file_format',
            field=models.CharField(default='PDF', max_length=10),
        ),
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='num_pages',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='year',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

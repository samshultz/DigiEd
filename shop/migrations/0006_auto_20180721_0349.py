# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-21 02:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_book_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ('-created',)},
        ),
    ]
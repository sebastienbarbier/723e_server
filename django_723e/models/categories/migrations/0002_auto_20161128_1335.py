# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-28 13:35
from __future__ import unicode_literals

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='color',
            field=colorfield.fields.ColorField(default=b'#ffffff', max_length=10),
        ),
    ]

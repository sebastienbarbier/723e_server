# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-17 02:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20160920_0849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='debitscredits',
            name='foreign_amount',
        ),
        migrations.RemoveField(
            model_name='debitscredits',
            name='foreign_currency',
        ),
    ]

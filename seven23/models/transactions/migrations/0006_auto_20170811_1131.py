# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-11 11:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_auto_20170811_1048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paidby',
            old_name='paid_by',
            new_name='attendee',
        ),
    ]

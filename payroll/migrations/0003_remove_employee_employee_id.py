# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 01:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0002_auto_20160419_0857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='employee_id',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-18 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='employeeId',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-25 09:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0010_auto_20160523_1313'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['modifyDateTime']},
        ),
        migrations.AddField(
            model_name='post',
            name='modifyDateTime',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 5, 25, 9, 20, 52, 245531, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='employeeId',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]

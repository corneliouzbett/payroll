# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 00:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.CharField(max_length=4, primary_key=True, serialize=False, verbose_name='\u90e8\u95e8\u7f16\u53f7')),
                ('department_name', models.CharField(max_length=20, unique=True, verbose_name='\u90e8\u95e8\u540d\u79f0')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='\u5458\u5de5\u59d3\u540d')),
                ('employee_id', models.CharField(max_length=20, unique=True, verbose_name='\u5458\u5de5\u53f7')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('phone_number', models.CharField(max_length=20, verbose_name='phone_number')),
                ('salary_rate', models.FloatField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Employee_type',
            fields=[
                ('employee_type_id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='\u5458\u5de5\u79cd\u7c7b\u53f7')),
                ('employee_type', models.CharField(max_length=20, unique=True, verbose_name='\u5458\u5de5\u79cd\u7c7b')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.Employee_type'),
        ),
    ]
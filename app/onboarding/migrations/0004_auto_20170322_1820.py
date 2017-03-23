# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0003_auto_20170322_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='phone_number',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, unique=True, verbose_name='Phone number'),
        ),
    ]
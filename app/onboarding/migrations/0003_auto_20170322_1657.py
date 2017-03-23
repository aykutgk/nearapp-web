# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 16:57
from __future__ import unicode_literals

from django.db import migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding', '0002_auto_20170322_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='phone_number',
            field=localflavor.us.models.PhoneNumberField(blank=True, default=None, max_length=20, null=True, unique=True),
        ),
    ]
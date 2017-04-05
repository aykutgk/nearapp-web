# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 02:01
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0009_auto_20170403_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Latitude/Longitude on Map'),
        ),
    ]

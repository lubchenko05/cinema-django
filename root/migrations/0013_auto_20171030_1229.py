# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 12:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0012_auto_20171030_1227'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CinemaPlaces',
            new_name='CinemaPlace',
        ),
        migrations.RenameModel(
            old_name='FilmSessionPlaces',
            new_name='FilmSessionPlace',
        ),
    ]
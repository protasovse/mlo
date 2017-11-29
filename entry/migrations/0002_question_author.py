# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 17:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mlo_auth', '0001_initial'),
        ('entry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='question', to='mlo_auth.User'),
        ),
    ]

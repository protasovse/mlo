# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 07:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0009_remove_question_answer_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='like_count',
            field=models.IntegerField(db_index=True, default=0, editable=False, verbose_name='Лайки'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='reply_count',
            field=models.IntegerField(db_index=True, default=0, editable=False, verbose_name='Количество ответов'),
        ),
        migrations.AlterField(
            model_name='question',
            name='like_count',
            field=models.IntegerField(db_index=True, default=0, editable=False, verbose_name='Лайки'),
        ),
        migrations.AlterField(
            model_name='question',
            name='reply_count',
            field=models.IntegerField(db_index=True, default=0, editable=False, verbose_name='Количество ответов'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 08:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mlo_auth', '0001_initial'),
        ('entry', '0006_auto_20171123_0712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('pub_date', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Дата публикации')),
                ('status', models.IntegerField(choices=[(0, 'Удалённый'), (1, 'Черновик'), (2, 'Опубликован')], db_index=True, default=2, verbose_name='Статус')),
                ('like_count', models.IntegerField(default=0, editable=False, verbose_name='Лайки')),
                ('answer_count', models.IntegerField(default=0, editable=False, verbose_name='Количество ответов')),
                ('entry_id', models.PositiveIntegerField(db_index=True)),
                ('author', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='answer_set', to='mlo_auth.User')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='entry.Answer')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('answers', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='comment_count',
        ),
    ]

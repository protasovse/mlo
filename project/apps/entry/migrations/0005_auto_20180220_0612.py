# Generated by Django 2.0 on 2018-02-20 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0004_auto_20180215_1844'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='likes',
            options={'verbose_name': 'Отметка «Полезно»', 'verbose_name_plural': 'Отметки «Полезно»'},
        ),
        migrations.AddField(
            model_name='likes',
            name='value',
            field=models.SmallIntegerField(default=1, verbose_name='Балл'),
            preserve_default=False,
        ),
    ]

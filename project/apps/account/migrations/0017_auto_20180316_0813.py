# Generated by Django 2.0.2 on 2018-03-16 05:13

from django.db import migrations
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_remove_info_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='type',
            field=django_mysql.models.EnumField(choices=[('Электронный ящик', 'Электронный ящик'), ('Телефон', 'Телефон'), ('Адрес', 'Адрес'), ('Сайт', 'Сайт'), ('Skype', 'Skype'), ('WhatsApp', 'WhatsApp'), ('Telegram', 'Telegram')], db_index=True, verbose_name='Тип'),
        ),
    ]

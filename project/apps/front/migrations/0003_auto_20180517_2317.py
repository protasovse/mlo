# Generated by Django 2.0.2 on 2018-05-17 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0002_auto_20180517_2315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citymeta',
            old_name='city_id',
            new_name='city',
        ),
    ]
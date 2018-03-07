# Generated by Django 2.0 on 2018-03-02 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20180219_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='finish',
            field=models.DateField(blank=True, help_text='Если не введено, то по настоящее время', null=True, verbose_name='Окончание работы'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='start',
            field=models.DateField(verbose_name='Начало работы'),
        ),
    ]
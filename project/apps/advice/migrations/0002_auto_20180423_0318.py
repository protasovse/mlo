# Generated by Django 2.0.2 on 2018-04-23 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advice',
            name='cost',
            field=models.PositiveIntegerField(default=1, verbose_name='Цена консультации'),
        ),
    ]

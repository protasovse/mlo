# Generated by Django 2.0.2 on 2018-03-25 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0017_auto_20180325_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='phone',
            field=models.CharField(blank=True, max_length=15, verbose_name='Телефон'),
        ),
    ]

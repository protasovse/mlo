# Generated by Django 2.0.2 on 2018-03-31 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0023_auto_20180330_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='first_name',
            field=models.CharField(blank=True, max_length=32, verbose_name='first name'),
        ),
    ]

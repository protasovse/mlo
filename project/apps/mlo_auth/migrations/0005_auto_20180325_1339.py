# Generated by Django 2.0.2 on 2018-03-25 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlo_auth', '0004_user_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=15, verbose_name='Телефон'),
        ),
    ]
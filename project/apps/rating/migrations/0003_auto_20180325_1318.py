# Generated by Django 2.0.2 on 2018-03-25 10:18

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0002_auto_20180322_2105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'ordering': ('-month_rate',), 'verbose_name': 'Рейтинг', 'verbose_name_plural': 'Рейтинг'},
        ),
        migrations.AlterModelManagers(
            name='rating',
            managers=[
                ('lawyers', django.db.models.manager.Manager()),
            ],
        ),
    ]
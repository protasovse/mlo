# Generated by Django 2.0.2 on 2018-03-20 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_rating_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='description',
            field=models.TextField(blank=True, max_length=1024, null=True, verbose_name='Описание организации'),
        ),
    ]

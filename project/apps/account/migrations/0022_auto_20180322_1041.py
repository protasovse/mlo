# Generated by Django 2.0.2 on 2018-03-22 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_auto_20180320_1005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='type',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.RemoveField(
            model_name='ratingresult',
            name='user',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.DeleteModel(
            name='RatingResult',
        ),
        migrations.DeleteModel(
            name='RatingTypes',
        ),
    ]

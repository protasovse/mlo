# Generated by Django 2.0 on 2017-12-19 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sxgeo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cities',
            name='region_id',
            field=models.IntegerField(db_index=True),
        ),
    ]

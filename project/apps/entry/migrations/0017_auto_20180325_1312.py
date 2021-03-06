# Generated by Django 2.0.2 on 2018-03-25 10:12

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('sxgeo', '0004_cities_is_main_city'),
        ('entry', '0016_auto_20180320_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sxgeo.Cities'),
        ),
        migrations.AddField(
            model_name='question',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, verbose_name='Телефон'),
        ),
    ]

# Generated by Django 2.0.2 on 2018-04-10 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0030_auto_20180407_1105'),
    ]

    operations = [
        migrations.CreateModel(
            name='SphCounter',
            fields=[
                ('counter_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('max_id', models.IntegerField()),
            ],
        ),
    ]

# Generated by Django 2.0.2 on 2018-04-11 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rubric', '0010_rubric_keywords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rubric',
            name='is_public',
        ),
    ]

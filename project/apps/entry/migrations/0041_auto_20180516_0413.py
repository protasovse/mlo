# Generated by Django 2.0.2 on 2018-05-16 01:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_auto_20180423_0318'),
        ('entry', '0040_auto_20180509_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='dir',
        ),
        migrations.RemoveField(
            model_name='article',
            name='entry_ptr',
        ),
        migrations.RemoveField(
            model_name='article',
            name='rubric',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='Dir',
        ),
    ]

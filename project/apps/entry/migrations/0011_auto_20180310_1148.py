# Generated by Django 2.0.2 on 2018-03-10 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0010_auto_20180310_0815'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='likes',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='likes',
            name='entry',
        ),
        migrations.RemoveField(
            model_name='likes',
            name='user',
        ),
        migrations.RemoveField(
            model_name='review',
            name='like',
        ),
        migrations.AlterModelTable(
            name='question',
            table=None,
        ),
        migrations.DeleteModel(
            name='Likes',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
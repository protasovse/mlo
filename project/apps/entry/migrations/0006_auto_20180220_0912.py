# Generated by Django 2.0 on 2018-02-20 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0005_auto_20180220_0612'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consult',
            old_name='experts',
            new_name='expert',
        ),
    ]

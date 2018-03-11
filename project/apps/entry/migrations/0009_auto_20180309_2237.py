# Generated by Django 2.0.2 on 2018-03-09 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0008_auto_20180307_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='like',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='entry.Likes'),
        ),
        migrations.AlterModelTable(
            name='question',
            table='entry_question',
        ),
    ]
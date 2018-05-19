# Generated by Django 2.0.2 on 2018-04-23 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_auto_20180328_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entry.Entry', verbose_name='Ответ'),
        ),
        migrations.AlterField(
            model_name='review',
            name='like',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='review.Likes'),
        ),
    ]
# Generated by Django 2.0 on 2018-02-18 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mlo_auth', '0002_auto_20180206_0951'),
        ('account', '0007_auto_20180218_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(db_index=True, verbose_name='Балл')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mlo_auth.User', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Рейтинг: результаты',
                'verbose_name_plural': 'Рейтинг: результаты',
            },
        ),
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'Рейтинг: балл', 'verbose_name_plural': 'Рейтинг: баллы'},
        ),
        migrations.AlterModelOptions(
            name='ratingtypes',
            options={'verbose_name': 'Рейтинг: тип', 'verbose_name_plural': 'Рейтинг: типы'},
        ),
        migrations.AlterField(
            model_name='rating',
            name='date',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='value',
            field=models.IntegerField(editable=False, verbose_name='Балл'),
        ),
        migrations.AlterField(
            model_name='ratingtypes',
            name='value',
            field=models.IntegerField(verbose_name='Балл'),
        ),
    ]

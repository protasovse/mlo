# Generated by Django 2.0.2 on 2018-03-06 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_remove_info_phone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='info',
            options={'verbose_name': 'Профиль юриста', 'verbose_name_plural': 'Профили юристов'},
        ),
        migrations.RemoveField(
            model_name='ratingresult',
            name='id',
        ),
        migrations.AlterField(
            model_name='ratingresult',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mlo_auth.User', verbose_name='Пользователь'),
        ),
    ]

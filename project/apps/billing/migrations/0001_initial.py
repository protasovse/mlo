# Generated by Django 2.0.2 on 2018-04-01 14:05

from django.db import migrations, models
import django.db.models.fields
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mlo_auth', '0006_user_is_expert'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(verbose_name='Значение')),
                ('date', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Дата перевода')),
                ('comment', models.CharField(max_length=256, verbose_name='Наименование платежа')),
            ],
            options={
                'verbose_name': 'История платежей',
                'verbose_name_plural': 'Истории платежей',
            },
        ),
        migrations.CreateModel(
            name='Purse',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.fields.NOT_PROVIDED, primary_key=True, serialize=False, to='mlo_auth.User', verbose_name='Пользователь')),
                ('balance', models.IntegerField(default=0, verbose_name='Текущий баланс')),
            ],
            options={
                'verbose_name': 'Кошелёк',
                'verbose_name_plural': 'Кошельки',
            },
        ),
        migrations.AddField(
            model_name='history',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.fields.NOT_PROVIDED, to='mlo_auth.User', verbose_name='Пользователь'),
        ),
    ]
